#-*- coding: utf-8 -*-
from django.db import models
from stock import *

class Unit(models.Model):
	"""
	Descrive una unità.
	vedi https://github.com/route-nazionale/meal-provision/wiki/Glossario
	"""
	vclan = models.CharField(max_length=30) # es SULMONA 1
	vclanID = models.CharField(max_length=30) # es B1747-T1
	unitaID = models.CharField(max_length=30, default='T1') # es T1
	gruppoID = models.CharField(max_length=30) # es B1747

	quartier = models.ForeignKey(Quartier) # int from 1 to 7, subcamps
	storeroom = models.ForeignKey(Storeroom)
	stock = models.ForeignKey(Stock) # from A to Z (22 letters)

	def __unicode__(self):
		return self.vclan + "-" + self.unitaID