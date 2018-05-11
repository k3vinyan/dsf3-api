# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
import requests
from . import helpers
from bs4 import BeautifulSoup
from models import Block, Route, Driver, Tba
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

# Create your views here.
@csrf_exempt
def drivers(request):
    if request.method == 'GET':
        data = serializers.serialize("json", Driver.objects.all())

        return HttpResponse(data, content_type='application/json')

    if request.method == 'POST':
        req = json.loads(request.body)

        for item in req:

            name = item['driverName'].split(" ")
            firstName = name[0]
            lastName = name[1]

            id = item['driverId']
            startTime = item['driverStartTime']
            endTime = item['driverEndTime']
            time = item['driverBlockTime']

            try:
                Block.objects.get(startTime=startTime)
            except:
                block = Block(startTime=startTime, endTime=endTime, shiftLength=time)
                block.save()
            try:
                Driver.objects.get(DPID=id)
            except ObjectDoesNotExist:
                block = Block.objects.get(startTime=startTime)
                driver = Driver(DPID=id,
                                firstName = firstName,
                                lastName = lastName,
                                shiftLength = time,
                                startTime = startTime,
                                endTime = endTime,
                                block = block
                                )
                driver.save()

        return HttpResponse("Kevin is the greatest of all time --drivers")

@csrf_exempt
def tbas(request):
    if request.method == 'GET':

        data = serializers.serialize("json", Tba.objects.all())

        return HttpResponse(data, content_type='application/json')

    if request.method == 'POST':
        req = json.loads(request.body)

        print req
        for item in req:

            tba = item['tba']
            link = item['link']
            status = item['status']
            city = item['city']
            zipCode = item['zipCode']
            route = item['route']
            associate = item['associate']
            sortZone = item['sortZone']
            address = item['address']

            if route != "" or route != None:
                try:
                    Route.objects.get(route=route)
                except ObjectDoesNotExist:
                    cluster = filter(lambda x: x.isalpha(), route)
                    route = Route(
                                    route=route,
                                    cluster = cluster,
                                    tbaCount = 0
                                )
                    route.save()
                try:
                    Tba.objects.get(tba=tba)
                except ObjectDoesNotExist:
                    routeToUpdate = Route.objects.get(route=route)
                    tba = Tba(
                        tba=tba,
                        link=link,
                        status=status,
                        city=city,
                        route=routeToUpdate,
                        zipCode=zipCode,
                        sortZone=sortZone,
                        address=address
                    )
                    tba.save()

                    routeToUpdate.update(tbas=ListF('tbas').append(tba))

            else:
                tba = Tba(
                    tba=tba,
                    link=link,
                    status=status,
                    city=city,
                    zipCode=zipCode,
                    sortZone=sortZone,
                    address=address
                )
                tba.save()

    return HttpResponse("Kevin is the greatest of all time --tbas")

@csrf_exempt
def routes(request):
    if request.method == 'GET':
        data = serializers.serialize("json", Route.objects.all())
        return HttpResponse(data, content_type='application/json')

    if request.method == 'POST':
        req = json.loads(request.body)

    return HttpResponse("Kevin is the greatest of all time --routes")
@csrf_exempt
def blocks(request):
    if request.method == 'GET':
        data = serializers.serialize("json", Block.objects.all())

        return HttpResponse(data, content_type='application/json')

    if request.method == 'POST':
        req = json.loads(request.body)

    return HttpResponse("Kevin is the greatest of all time --blocks")




#for development only, tests
# def roster(request):
#     return render(request, 'drivers/test-roster.html')
