from bs4 import BeautifulSoup
from django.http import HttpResponse
from urllib2 import urlopen, HTTPError, URLError, HTTPRedirectHandler
import requests, re
import Cookie
from collections import OrderedDict
import datetime
import os

URLS = {
    "SEARCH": 'https://www.amazonlogistics.com/comp/packageSearch',
    "SIGNIN": "https://www.amazonlogistics.com/ap/signin",
    "BASE": "https://www.amazonlogistics.com/",
    "ROSTER": "https://logistics.amazon.com/internal/capacity/rosterview?serviceAreaId=11&date="
}

userSession = {
    "session": ""
}

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"en-US, en;q=0.9",
    "Content-Type":"application/x-www-form-urlencoded",
    "Accept":"text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,*/*;q=0.8"
}

searchForm = {
    'dateType':"shipDate",
    'shipStartDate':"02/07/2018",
    'shipStartTime':"00:00",
    'shipEndDate':"02/10/2018",
    'shipEndTime':"00:00",
    'deliveryStartDate':"02/09/2018",
    'deliveryStartTime':"00:00",
    'deliveryEndDate':"02/10/2018",
    'deliveryEndTime':"00:00",
    'scheduledStartDateBegin':"02/09/2018",
    'scheduledStartTimeBegin':"00:00",
    'scheduledStartDateEnd':"02/10/2018",
    'scheduledStartTimeEnd':"00:00",
    'shipStatusIdList':"AT_STATION",
    'shipmentStationHolder':"1002821",
    'shipmentAssociateHolder':"ALL",
    'shipType':"ALL",
    'shipOption':"ALL",
    'shipmentSearchId':"",
    'shipmentSearchIds':"",
    'shipmentSearchPhone':"",
    'downloadToken': "",
    'downloadToken': "",
    'ec_i':"ShipmentListTable",
    'ShipmentListTable_crd':"2000",
    'ShipmentListTable_p':"1",
    'ShipmentListTable_s_merchantId':"",
    'ShipmentListTable_a_manifestTrackingId':"shipmentTrackingId",
    'ShipmentListTable_a_shipOption':"shipOptionName",
    'ShipmentListTable_a_shipType':"shipmentTitle",
    'ShipmentListTable_a_stationName':"holderStationName",
    'ShipmentListTable_a_associateHolder':"holderEmployeeName",
    'ShipmentListTable_rd':"50",
    'action':"ajaxSearch"
}

def getRosterUrl():
    return URLS["ROSTER"] + str(datetime.date.today())

#get session from comp
def getAmazonSession():
    session = requests.Session()
    s = session.get(URLS['SEARCH'], headers=headers)

    BSObj = BeautifulSoup(s.text, 'lxml')
    hiddenInput = BSObj.select('input[type="hidden"]')
    params = {}
    for item in hiddenInput:
        try:
            params[item['name']] = item['value']
        except KeyError:
            params[item['name']] = ""

    params['email'] = os.getenv("EMAIL")
    params['password'] = os.getenv("PASSWORDFOREMAIL")

    response = session.post(URLS['SIGNIN'], data=params, headers=headers)
    return session

    for item in params:
        print item + ": " + params[item]

def getRoutingToolsData(cluster):

    #Avaiable Cluster
    DSF3_EMERGENCY  = "#graph-DSF3_EMERGENCY"
    RTS_DSF3_LATE   = "#graph-RTS-DSF3-LATE"
    SAME_EVEN       = "#graph-DSF3-SAME-EVEN"

    #tuple of package status
    packageStatus = ('betweenFCandStation', 'atStation', 'readyForDeparture', 'onRoadWithDA', 'delivered', 'attempted', 'undelivered', 'others')

    s = requests.get("http://localhost:8000/checkout/routingTools", headers=headers)
    #create session and create soup object
    BSObj = BeautifulSoup(s.text, 'lxml')

    #
    #get all routes for cluster and return dictionary of routes
    def getRoutes(cluster):
        #routes = BSObj.select(cluster)[0].find_all("text", attrs={"style":"text-anchor: end;", "x":"-9", "y":"0"})
        routes = BSObj.select(cluster)[0].find_all("text", attrs={"dy":".32em", "style":"text-anchor: end;"})
        routesDict = OrderedDict()
        for route in routes:
            routesDict[route.text] = {}
        return routesDict

    #get the values from the status of each route; return array of tuples
    def getValueOfStatus(cluster):
        data = []
        sort = []

        values = BSObj.select(cluster)[0].find_all("text", attrs={"dy":".40em", "text-anchor":"middle", "font-size":"12px"})
        count = 0
        for value in values:
            count += 1
            sort.append(value.text)
            if count == 8:
                count = 0
                data.append(tuple(sort))
                sort = []
        return data

    def createClusterData(getValueOfStatus, getRoutes, packageStatus):
        newObject = {}
        for data, route in zip(getValueOfStatus, getRoutes):
            newObject[route] ={}
            for value, status in zip(data, packageStatus):
                newObject[route][status] = value
        return newObject

    #use multiple methods to create object of allroutes data from routingTools
    def getRouteToolsData(cluster):
        valueOfStatus = getValueOfStatus(cluster)
        routes = getRoutes(cluster)

        clusterData = createClusterData(valueOfStatus, routes, packageStatus)
        return clusterData

#search amazon comp and return search tbas
def getTbasFromComp(session, form):
    response = session.post(URLS['SEARCH'], data=form, headers=headers)
    #response = requests.post(URLS['SEARCH'], data=form, headers=headers, cookies=cookies)
    BSObj = BeautifulSoup(response.text, 'lxml')
    tbaList = []
    odd = BSObj.select('tr[class="odd"]')
    even = BSObj.select('tr[class="even"]')
    #find tba, link, route, and status
    for item in odd:
        tdList = item.select('td')

        tba = item.find('a').text
        link = item.find('a').get('href')
        route = item.select('.routeCode')[0].text
        status = item.select('.sm_status')[0].text
        address = tdList[12].text


        tbaInfo = {}
        driver = {'firstName': "", 'lastName': ""}
        tbaInfo['driver'] = driver
        tbaInfo['tba'] = tba
        tbaInfo['link'] = URLS['BASE'] + link
        tbaInfo['route'] = route
        tbaInfo['status'] = status
        tbaInfo['address'] = address
        tbaList.append(tbaInfo)

    for item in even:
        tdList = item.select('td')

        tba = item.find('a').text
        link = item.find('a').get('href')
        route = item.select('.routeCode')[0].text
        status = item.select('.sm_status')[0].text
        address = tdList[12].text

        tbaInfo = {}
        driver = {'firstName': "", 'lastName': ""}
        tbaInfo['driver'] = driver
        tbaInfo['tba'] = tba
        tbaInfo['link'] = URLS['BASE'] + link
        tbaInfo['route'] = route
        tbaInfo['status'] = status
        tbaInfo['address'] = address
        tbaList.append(tbaInfo)

    return tbaList
