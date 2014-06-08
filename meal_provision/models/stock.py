from django.db import models
from django.core.validators import *

class Quartier(models.Model):
	"""Models quartier (sottocampo) """
	number = models.IntegerField(
			validators=[
				MinValueValidator(1),
				MaxValueValidator(5)
			]
		)
	color = models.CharField(max_length=50)
	storerooms_number = models.IntegerField()

	def __unicode__(self):
		return self.color

class Storeroom(models.Model):
	"""Models storeroom (magazzino)"""
	quartier = models.ForeignKey(Quartier)
	number = models.IntegerField(default = 1,
			validators=[
				MinValueValidator(1),
				MaxValueValidator(5)
			]
		)

	def __unicode__(self):
		return self.quartier.__unicode__() + "-" + str(self.number);

class Stock(models.Model):
	""" Models stock point (stoccaggio) within storerooms"""
	letter = models.CharField(max_length=1,
			validators=[
				RegexValidator(
						r"[A-Z]{1}"
					)
			]
		)
	box_number = models.IntegerField()
	storeroom = models.ForeignKey(Storeroom)
	quartier = models.ForeignKey(Quartier)

	def __unicode__(self):
		return self.storeroom.__unicode__() + "-" + self.letter;

