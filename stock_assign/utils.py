#-*- coding: utf-8 -*-
from meal_provision.models.order import *
from globals import *

######################################################
#				CSV UTILS				  			 #
######################################################

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
def make_csv_record_from_map(m):
	ret = []
	for i in COLUMNS:
		if i in m:
			ret.append(m[i])
		else:
			ret.append("null")
	return ret


# todo: nel file finale i giorni vengono stampati due volte
## [string]
def make_csv_titles():
	t = TITLES_LIST
	# {}/08/14-Col
	for i in route_days:
		for j in meals_names:
			t.append('{}/08/14-{}'.format(i,j))
	return t

def make_csv_record(p):
	en = enumerate_meals( int(p.from_day), int(p.to_day), int(p.from_meal), int(p.to_meal))
	ms = print_meals(p.std_meal, p.col, en)
	l = p.as_list()
	l.extend(ms)
	return l

def all_csv_records_iterator():
	# todo calcolare quanti sono i ps
	ps = list(Person.objects.all().prefetch_related('unit'))	
	t = make_csv_titles()
	yield t
	for p in ps:
		yield make_csv_record(p)
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

# todo: enumerate_meals maybe substituted with a range XD
def enumerate_meals(from_day, to_day, from_meal, to_meal):
	return range(
		meal_number(from_day,from_meal),
		meal_number(to_day,to_meal) + 1
	)

# todo handle exceptions

def test_enumerate_meals():
	r = enumerate_meals(6, 10, 2, 2)
	return r

def test_print_meals():
	return print_meals('standard', 'latte', enumerate_meals(5,10,1,2))

##################################################################
#				  Virtual 	person 								 #
##################################################################

def genera_persone_virtuali(num,from_d, to_d, meal):
	for i in range(0,num):
		VirtualPerson(from_day=from_d,to_day=to_d,std_meal=meal).save()

def set_all_to_camst():
	ps = Person.objects.all()
	for p in ps:
		tc = CamstControl(person=p)
		tc.save()
