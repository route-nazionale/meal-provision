from django.db import models
from stock import *

class Unit(models.Model):
	vclan = models.CharField(max_length=30)
	vclanID = models.CharField(max_length=30)
	unitaID = models.CharField(max_length=30, default='T1')
	gruppoID = models.CharField(max_length=30)

	quartier = models.ForeignKey(Quartier) # int from 1 to 7, subcamps
	storeroom = models.ForeignKey(Storeroom)
	stock = models.ForeignKey(Stock) # from A to Z (22 letters)

	def __unicode__(self):
		return self.vclan + "-" + self.unitaID