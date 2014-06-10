#-*- coding: utf-8 -*-
from django.db import models
from clanfuoco import *
from stock import *
#from stock_assign.utils import stringify_col, stringify_meal

# Order is a line in the final orders file
class Person(models.Model):
	
	code = models.IntegerField()
	unit = models.ForeignKey(Unit)

	tipo_codice = models.CharField(max_length=50)
	intolleranze_allergie = models.CharField(max_length=100, null=True)

	std_meal = models.CharField(max_length=50, default="standard")
	col = models.CharField(max_length=20, default="latte")
	
	from_day = models.IntegerField(default=1)
	to_day = models.IntegerField(default=1)
	from_meal = models.IntegerField(default=0) # 0 = colazione, 1 = pranzo, 2 = cena
	to_meal = models.IntegerField(default=2)
	
	def __unicode__(self):
		return str(self.code)


	def as_map(self):
		return {
			'code' : str(self.code),
			'quartier' : str(self.unit.quartier.number),
			'storeroom': str(self.unit.storeroom.number),
			'stock' : self.unit.stock.letter,
			'code-type' : self.tipo_codice,
			'allergies' : self.intolleranze_allergie,
			'std_meal' : self.std_meal,
			'col' : self.col,
			'group' : self.unit.gruppoID,
			'unitid' : self.unit.unitaID,
			'vclanid' : self.unit.vclanID,
			'vlcan' : self.unit.vclan + "-" + self.unit.unitaID,
			# 'from_day' : self.from_day,
			# 'to_day' : self.to_day,
			# 'from_meal' : self.from_meal,
			# 'to_meal' : self.to_meal
		}

	## todo: validators?

class CamstControl(models.Model):
	to_camst = models.BooleanField(default=True)
	person = models.ForeignKey(Person)

class VirtualPerson(models.Model):

	from_day = models.IntegerField(default=1)
	to_day = models.IntegerField(default=1)
	from_meal = models.IntegerField(default=0) # 0 = colazione, 1 = pranzo, 2 = cena
	to_meal = models.IntegerField(default=2)

	std_meal = models.CharField(max_length=50, default="standard")
	col = models.CharField(max_length=20, default="latte")

	to_camst = models.BooleanField(default=True)

	quartier = 6
	storeroom = 1
	stock = 'A'

	def as_map(self):
		u = Unit.objects.filter(vclan="oneteam")[0]
		return {
			"code" :"x-" + str(self.id),
			"quartier" : str(self.quartier),
			"storeroom" : str(self.storeroom),
			"stock" : self.stock,
			'group' : u.gruppoID,
			'code-type' : 'scout',
			'allergies' : 'nessuna',
			'unitid' : u.unitaID,
			'vclanid' : u.vclanID,
			'vlcan' : u.vclan,

		}
