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
def make_csv_record(m):
	ret = []
	for i in COLUMNS:
		if i in m:
			ret.append(m[i])
		else:
			ret.append("null")
	return ret

## [string]
def make_csv_titles():
	t = make_csv_record(TITLES)
	# {}/08/14-Col
	j = 0
	for i in route_days:
		for j in meals_names:
			t.append('{}/08/14-{}'.format(i,j))
	return t

def make_all_records():
	# t_c = CamstControl.objects.filter(to_camst=True)
	pp = Person.objects.all()
	#for c in t_c:
	#	pp.append(c.person)
	vv = VirtualPerson.objects.all()
	tit = make_csv_titles()
	mm = []
	mm.append(tit)
	for p in pp:
		en = enumerate_meals( p.from_day, p.to_day, p.from_meal, p.to_meal)
		ms = print_meals(p.std_meal, p.col, en)
		rec = make_csv_record(p.as_map())
		rec.extend(ms)
		mm.append(rec)
	for v in vv:
		en = enumerate_meals( v.from_day, v.to_day, v.from_meal, v.to_meal)
		ms = print_meals(v.std_meal, v.col, en)
		rec = make_csv_record(v.as_map())
		rec.extend(ms)
		mm.append(rec)
	return mm

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
	""" construct list """
	ret = []
	d = from_day
	m = from_meal
	
	# first day, append meals since arrival
	while m <= max(meals_types):
		ret.append(meal_number(d,m))
		m+=1
	d+=1

	# internal day, append all meals in a day
	while d < to_day:
		for meal in meals_types:
			ret.append(meal_number(d,meal))
			meal += 1
		d+=1

	# last day, append meals until departure
	m = meals_types[0]
	while m <= to_meal:
		ret.append(meal_number(d,m))
		m+=1

	return ret

# todo handle exceptions

def test_enumerate_meals():
	r = enumerate_meals(5, 10, 1, 2)
	return r

def test_print_meals():
	return print_meals('standard', 'latte', enumerate_meals(5,10,1,2))

##################################################################
#				  Virtual 	person 								 #
##################################################################

#def genera_persone_virtuali(num=1,from=4, to=13, meal="standard", col="latte"):
	#for i in range(0,num):
		#VirtualPerson()

def set_all_to_camst():
	ps = Person.objects.all()
	for p in ps:
		tc = CamstControl(person=p)
		tc.save()