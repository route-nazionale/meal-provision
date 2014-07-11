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

	size = models.IntegerField(default=0)
	regione = models.CharField(max_length=50)

	raggruppamento_trasporti = models.CharField(max_length=50)

	quartier = models.ForeignKey(Quartier) # int from 1 to 7, subcamps
	storeroom = models.ForeignKey(Storeroom)
	#stock = models.ForeignKey(Stock) # from A to Z (22 letters)

	## todo: retrieve number of people in the unit in a more performant way
	def people_count(self):
		return self.size

	def assign(self, st):
		if (st.storeroom != self.storeroom):
			raise Error("Assignamento di un'unità in un altro sottocampo")
		a = StockAssignement(unit=self,stock=st)
		a.save()

	def __unicode__(self):
		return self.vclan + "-" + self.unitaID

class StockAssignement(models.Model):
	unit = models.ForeignKey(Unit)
	stock = models.ForeignKey(Stock)
