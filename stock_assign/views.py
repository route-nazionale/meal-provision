#-*- coding: utf-8 -*-
from django.shortcuts import HttpResponse, render
from django.http import StreamingHttpResponse
from django.template import RequestContext, loader
from models import *
from utils import *
from unicodecsv import writer

def index(request):
	"""
	Home page di stock assign. Contiene links alle altre view
	"""
	t = loader.get_template("home.html")
	c = RequestContext(request)
	return HttpResponse(t.render(c))

def list_stocks(request):
	"""
	Stampa una lista di tutti i punti di stoccaggio/distribuzione
	vedi https://github.com/route-nazionale/meal-provision/wiki/Glossario
	"""
	# todo: migliorare la presentazione, aggiungere quanti clan
	# nota: il contenuto della 
	ss = Stock.objects.all().prefetch_related('quartier','storeroom')
	res = []
	for s in ss:
		res.append(s.__unicode__() + "<br>\n")

	return HttpResponse("<b>Stocks</b><br>" + "".join(res))

def list_all_orders(request):
	"""
	Un template per vedere una preview del file csv che viene
	generato
	"""

	# carica i dati
	rs = all_csv_records_iterator()
	l = len(rs)

	t = loader.get_template("exported_table.html")

	c = RequestContext(request)
	c['persons'] = rs
	c['number_of_records'] = l - 1

	return HttpResponse(t.render(c))

def list_orders_from_to(request, from_record, howmany):
	"""
	Restitusce lo stesso template di list_all_orders
	ma permette di filtrare i risultati
	"""
	# todo: bug: i record restituiti sono il doppio di howmany poichè la ricerca è fatta sia in Person che in VirtualPerson
	records = csv_records_iterator(howmany)
	
	person_count = (Person.objects.all()[:howmany]).count() 
	virtual_person_count = (VirtualPerson.objects.all()[:howmany]).count()
	total_count = person_count + virtual_person_count

	t = loader.get_template("exported_table.html")
	
	c = RequestContext(request)
	c['persons'] = records
	c['number_of_records'] = total_count
	c['frm'] = from_record
	c['to'] = howmany
	
	return HttpResponse(t.render(c))

def list_vpeople(request):
	"""
	Restitusce una lista delle persone virtuali nel database
	vedi https://github.com/route-nazionale/meal-provision/wiki/Glossario
	"""
	vv = VirtualPerson.objects.all()
	mm = []

	for v in vv:
		# en = enumerate_meals( v.from_day, v.to_day, v.from_meal, v.to_meal)
		# ms = print_meals(v.std_meal, v.col, en)
		# rec = make_csv_record(v)
		# rec.extend(ms)
		mm.append(v.as_list())

	t = loader.get_template("vpeople_table.html")

	c = RequestContext(request)

	c['persons'] = mm

	c['number_of_records'] = len(mm)

	return HttpResponse(t.render(c))

def all_orders_to_csv_iterator_writer(request):
	"""
	Risponde con un file csv contenente tutti i record.
	Utilizza il writer di unicodecsv (patchato) per
	creare una risposta in streaming in modo da diminuire il
	tempo iniziale di preparazione del download.
	"""
	# è un oggetto che simula un file ed espone un unico metodo write()
	# la classe Echo è definita in utils.py
	pseudo = Echo()

	# crea un CSV writer sul file fasullo
	w = writer(pseudo)

	# crea una risposta http streaming con l'iteratore sulle
	# scritture del record. 
	response = StreamingHttpResponse(

			# w.writerow() restituisce il valore scritto
			# perciò questo iteratore restituisce una lista
			# di righe del file CSV

			# qui utilizziamo un doppio iteratore:
			# sia iteriamo sulla generazione delle righe che su
			# la scrittura del csv
			(w.writerow(row) for row in all_csv_records_iterator()),

			content_type="text/csv"
		)

	response['Content-Disposition'] = 'attachment; filename="RN2014-Pasti.csv"'

	return response

def orders_to_csv_iterator_writer(request,frm, howmany):

	pseudo = Echo()

	w = writer(pseudo)

	response = StreamingHttpResponse(

			(w.writerow(row) for row in csv_records_iterator(howmany)),

			content_type="text/csv"
		)

	response['Content-Disposition'] = 'attachment; filename="RN2014-Pasti.csv"'

	return response

def show_day_counts(request):
	"""
	Restitusce una vista contenente una tabella con le somme degli
	ordini per ogni giorno e per ogni pranzo
	"""

	# Le query di django non hanno metodi per il group by perciò
	# si usa una query raw si per le persone che per le virtual
	ps = Person.objects.raw('''SELECT 
			id,COUNT(code) AS pcount, 
			to_meal, 
			from_meal,
			to_day,
			from_day,
			std_meal
		FROM meal_provision_person
		GROUP BY to_meal, from_meal,to_day,from_day,std_meal''')

	vs = Person.objects.raw('''SELECT 
			id,COUNT(id) AS pcount, 
			to_meal, 
			from_meal,
			to_day,
			from_day,
			std_meal
		FROM meal_provision_person
		GROUP BY to_meal, from_meal,to_day,from_day,std_meal''')

	sums = []
	# todo: implementare la logica per generare la tabella delle somme
			##  INSERIRE LOGICA DELLA VISTA ##

	t = loader.get_template("day_sums.html")
	c = RequestContext(request)
	c['sums'] = sums
	return HttpResponse(t.render(c))

def show_assignement():
	# todo: mostra assegnamento generato
	return HttpResponse("Assegnamento generato")

def new_assignement():
	# todo: trigger nuovo assegnamento
	return HttpResponse("Generato nuovo assegnamento. Visualizzalo")



