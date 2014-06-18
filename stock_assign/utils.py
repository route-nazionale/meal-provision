#-*- coding: utf-8 -*-
from meal_provision.models.order import *
from globals import *

######################################################
#				CSV UTILS				  			 #
######################################################

# La descrizione dei vari field per il file CSV
TITLES = {
	'code' : "Codice", 
	'quartier' : "Sottocampo",
	'storeroom' : "Magazzino",
	'stock' : "Stoccaggio",
	'group' : "Gruppo",
	'unitid' : "UnitaID",
	'vclanid' : "VclanID",
	'vlcan' : "Vclan",
	'code-type' : "Tipo-codice",
	'allergies' : "Intolleranze-Allergie",
}

# I nomi dei campi in una lista (order matter!)
TITLES_LIST = [
	"Codice", 
	"Sottocampo",
	"Magazzino",
	"Stoccaggio",
	"Gruppo",
	"UnitaID",
	"VclanID",
	"Vclan",
	"Tipo-codice",
	"Intolleranze-Allergie",
]

# L'ordine delle colonne nel file CSV
COLUMNS = [
	'code',
	'quartier',
	'storeroom',
	'stock',
	'group',
	'unitid',
	'vclanid',
	'vlcan',
	'code-type',
	'allergies',
]

meals_names = [
	'Colaz',
	'Pranzo',
	'Cena'
]

## [map] -> [string]
# Deprecated
def make_csv_record_from_map(m):
	"""
	Costruisce una lista con i valori nell'ordine
	dato da COLUMNS a partire dalla mappa di una Persona.
	"""
	ret = []
	for i in COLUMNS:
		if i in m:
			ret.append(m[i])
		else:
			ret.append("null")
	return ret


## [string]
def make_csv_titles():
	"""
	Costruisce la lista dei titoli per il file
	"""
	print("Costruisco i titoli")
	# prende la lista dei titoli
	t = TITLES_LIST

	# Per ogni giorno e per ogni pasto appende
	# alla lista dei titoli una descrizione
	# del tipo 04/08/14-Colaz
	for i in route_days:
		for j in meals_names:
			s = '{}/08/14-{}'.format(i,j)
			t.append(s)

	print("lunghezza dei titoli=" + str(len(t)))
	return t

def make_csv_record(p):
	en = enumerate_meals(
		int(p.from_day), 
		int(p.to_day), 
		int(p.from_meal), 
		int(p.to_meal),
		# deve avere il pranzo del 6?
		(p.tipo_codice != 'RS-SARDI' and p.tipo_codice != 'RS'),
		# deve avere la cena del 10?
		(p.tipo_codice == 'RS-FINE'),
	)
	ms = print_meals(p.std_meal, p.col, en)
	l = p.as_list()
	l.extend(ms)
	return l

def all_csv_records_iterator(filt=None, fval=None):
	# todo: calcolare quanti sono i ps
	if filt == 'codice':
		ps = list(Person.objects.filter(code=fval).prefetch_related('unit'))
	elif filt == 'unit':
		ps = list(Person.objects.filter(unit=fval).prefetch_related('unit'))
	elif filt == 'tipo-codice':
		ps = list(Person.objects.filter(tipo_codice=fval).prefetch_related('unit'))
	else:
		ps = list(Person.objects.all().prefetch_related('unit'))	

	t = make_csv_titles()
	yield t
	for p in ps:
		yield make_csv_record(p)

	if not filt:
		vs = list(VirtualPerson.objects.all())
		for v in vs:
			yield make_csv_record(v)

def csv_records_iterator(howmany):
	# todo: calcolare quanti sono i ps
	ps = list(Person.objects.all().prefetch_related('unit')[:howmany])	
	yield make_csv_titles()
	for p in ps:
		yield make_csv_record(p)
	vs = list(VirtualPerson.objects.all()[:howmany])
	for v in vs:
		yield make_csv_record(v)

class Echo(object):
	"""
	A class used as a fake file to the csv writer object.
	logs how many records are writter
	"""
	n = 0
	def write(self, val):
		self.n+=1
		print(self.n)
		return val

#######################################################
#				DAYS UTILS							  #
#######################################################

# returns - starting from zero - the index
# of the meal in order of time
def meal_number(d,m):
	return (d - 4) * 3 + m


def print_meals(std_meal, col, days):
	""" Returns a list of strings describing meal meals_types
	for every type in the event. List length is fixed and is the global all_meals.
	takes standard meal for a person, breackfast type and the list of days
	of presence in route.
	"""
	ret = []
	for i in all_meals:
		if i in days:
			if i % 3 == 0:
				ret.append(col)
			else:
				ret.append(std_meal)
		else:
			ret.append("0")
	return ret

def enumerate_meals(from_day, to_day, from_meal, to_meal, lunch6=True, dine10=True):
	r = range(
		meal_number(from_day,from_meal),
		meal_number(to_day,to_meal) + 1
	)
	l6 = meal_number(6,1)
	d10 = meal_number(10,2)

	# Trattamento speciale per il pranzo del 6
	if l6 in r and not lunch6:
		del r[r.index(l6)]

	# Trattamento speciale per la cena del 10
	if d10 in r and not dine10:
		del r[r.index(d10)]

	return r

##################################################################
#				  Virtual 	person 								 #
##################################################################

def genera_persone_virtuali(num,from_d, to_d, from_m, to_m, meal):
	for i in range(0,num):	
		VirtualPerson(
			from_meal=from_m,
			to_meal=to_m,
			from_day=from_d,
			to_day=to_d,
			std_meal=meal).save()

def set_all_to_camst():
	ps = Person.objects.all()
	for p in ps:
		tc = CamstControl(person=p)
		tc.save()


###################################################################

def people_5_evening():
	ps = Person.objects.raw("""SELECT id, unit_id  FROM `meal_provision_person` 
		WHERE `from_day` <= 5 
		AND `to_day` >= 6 
		AND `from_meal` <= 2
		AND `to_meal` >= 0
		GROUP BY unit_id""")
	for p in ps:
		print(p.unit.vclan + " " + p.unit.unitaID)

def people_6_lunch():
	ps = Person.objects.raw("""SELECT id, unit_id  FROM `meal_provision_person` 
		WHERE `from_day` <= 6
		AND `to_day` >= 6
		GROUP BY unit_id""")
	for p in ps:
		print(p.unit.vclan + " " + p.unit.unitaID)