from django.db import models

class Iscritto(models.Model):
   census_code = None
   surname = ""
   name = []
   food_intolerances = []
   patologies = []
   # management fields
   original_description = ""
   normalized = False
   original_description = ""
   normalized = False