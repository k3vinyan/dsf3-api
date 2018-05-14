# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Route(models.Model):
     route       = models.CharField(max_length=50)
     cluster     = models.CharField(max_length=50)
     isAssigned  = models.BooleanField(default=False)
     tbaCount    = models.CharField(max_length=50, blank=True)
     DP          = models.CharField(max_length=50, blank=True, null=True)
     create_at   = models.DateTimeField(auto_now_add=True, null=True)

     def __str__(self):
         return self.route

     class Meta:
         ordering = ('cluster', 'route',)

class Block(models.Model):
    date        = models.DateTimeField(max_length=50, blank=True, null=True)
    startTime   = models.CharField(max_length=50)
    endTime     = models.CharField(max_length=50)
    shiftLength = models.CharField(max_length=50)
    create_at   = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.startTime + " - " + self.endTime

class Driver(models.Model):
    DPID        = models.CharField(max_length=20, default=False)
    fullName    = models.CharField(max_length=40, blank=True)
    firstName  = models.CharField(max_length=20)
    lastName   = models.CharField(max_length=30)
    checkin     = models.BooleanField(default=False)
    isAssigned  = models.BooleanField(default=False)
    shiftLength = models.CharField(max_length=20, blank=True)
    startTime   = models.CharField(max_length=10, blank=True)
    endTime     = models.CharField(max_length=10, blank=True)
    isNoShow    = models.BooleanField(default=True)
    checkout    = models.BooleanField(default=False)
    packageScan = models.CharField(max_length=3, blank=True)
    routingTool = models.CharField(max_length=3, blank=True)
    route       = models.CharField(max_length=10, blank=True, null=True)
    block       = models.ForeignKey(Block, null=True)
    create_at   = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.firstName + " " + self.lastName

    class Meta:
        ordering = ('block', 'firstName',)

class Tba(models.Model):
    driver      = models.CharField(max_length=20, blank=True, null=True)
    route       = models.CharField(max_length=10, blank=True, null=True)
    tba         = models.CharField(max_length=20)
    status      = models.CharField(max_length=10)
    link        = models.CharField(max_length=25)
    address     = models.CharField(max_length=20, blank=True)
    city        = models.CharField(max_length=15, blank=True)
    zipCode     = models.CharField(max_length=20, blank=True)
    sortZone    = models.CharField(max_length=15, blank=True)
    create_at   = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.tba
