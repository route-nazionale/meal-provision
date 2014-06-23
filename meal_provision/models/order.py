
#-*- coding: utf-8 -*-
from django.db import models
from clanfuoco import *
from stock import *
#from stock_assign.utils import stringify_col, stringify_meal

# Order is a line in the final orders file
class Person(models.Model):
	
	# Codice censimento
	code = models.IntegerField()

	# Chiave esterna alla propria unità
	unit = models.ForeignKey(Unit)

	# Identifica il tipo di iscrizione
	tipo_codice = models.CharField(max_length=50)
	
	# Campo testuale con le allergie
	intolleranze_allergie = models.CharField(max_length=100, null=True)
	
	# Specifica se il pasto è standard, vegetariano o vegano
	std_meal = models.CharField(max_length=50, default="standard")
	
	# Specifica se latte, tè o altro
	col = models.CharField(max_length=20, default="latte")
	
	# Il primo giorno in cui consuma un pasto al campo
	from_day = models.IntegerField(default=1)

	# L'ultimo giorno in cui consuma un pasto al campo
	to_day = models.IntegerField(default=1)
	
	# Il primo pasto consumato al campo
	# 0 = colazione, 1 = pranzo, 2 = cena
	from_meal = models.IntegerField(default=0) 
	
	# L'ultimo pasto consumato al campo
	# 0 = colazione, 1 = pranzo, 2 = cena
	to_meal = models.IntegerField(default=2)
	
	def __unicode__(self):
		return str(self.code)

	def as_map(self):
		"""
		Esporta i valori della persona come mappa
		"""
		# todo: sostituire con un metodo builtin di django?
		return {
			'code' : str(self.code),
			'quartier' : str(self.unit.quartier.number),
			'storeroom': str(self.unit.storeroom.number % 5 + 1),
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

	def as_list(self):
		"""
		Restiuisce i valori come lista. L'ordine è quello necessario
		nel file di esportazione.
		"""
		assigned = StockAssignement.objects.filter(unit=self.unit)
		if(len(assigned) < 1):
			letter = "?"
		else:
			letter = assigned.first().stock.letter
		return [
			str(self.code),
			str(self.unit.quartier.number),
			str(self.unit.storeroom.contrada_storeroom),
			letter,
			self.unit.regione,
			self.unit.gruppoID,
			self.unit.unitaID,
			self.unit.vclanID,
			self.unit.vclan,
			self.tipo_codice,
			self.intolleranze_allergie,
		]

	## todo: validators?

class CamstControl(models.Model):
	"""
	Una classe per controllare l'inserimento o meno di una persona nel
	file di export.
	Per lasciare intatta la tabella Person si una tabella accessoria
	con un booleano ed una chiave esterna

	ATTENZIONE: Non ancora implementato nel db
	"""
	# todo: popolare la tabella meal_provision_camstcontrol nel db!

	# Controllo sull'inserimento della persona
	to_camst = models.BooleanField(default=True)
	
	# La persona associata
	person = models.ForeignKey(Person)

class VirtualPerson(models.Model):
	"""
	Modella una persona virtuale.
	La tabella nel db è meal_provision_virtualperson
	vedi https://github.com/route-nazionale/meal-provision/wiki/Glossario
	"""

	# I nomi dei field hanno la stessa semantica che in Person
	# Ci sono meno field perchè tutte le persone virtuali afferiscono
	# allo stesso clan, non hanno allergie
	# Possono però avere colazioni o pasti differenti

	from_day = models.IntegerField(default=1)

	to_day = models.IntegerField(default=1)

	from_meal = models.IntegerField(default=0) # 0 = colazione, 1 = pranzo, 2 = cena
	
	to_meal = models.IntegerField(default=2)

	std_meal = models.CharField(max_length=50, default="standard")
	col = models.CharField(max_length=20, default="latte")

	tipo_codice = "OTX"

	# Per le persone virtuali il valore to_camst è inserito direttamente
	# nel modello
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
			'unitid' : u.unitaID,
			'vclanid' : u.vclanID,
			'vlcan' : u.vclan,
			'code-type' : self.tipo_codice,
			'allergies' : 'nessuna',
			'from_day' : self.from_day,
			'to_day' : self.to_day,
			'from_meal' : self.from_meal,
			'to_meal' : self.to_meal,
		}

	def as_list(self):
		u = Unit.objects.filter(vclan="oneteam")[0]
		return [
			"x-" + str(self.id),
			str(self.quartier),
			str(self.storeroom),
			self.stock,
			"SER",
			u.gruppoID,
			u.unitaID,
			u.vclanID,
			u.vclan,
			self.tipo_codice,
			'',
		]
