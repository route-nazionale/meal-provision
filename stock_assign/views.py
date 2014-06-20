#-*- coding: utf-8 -*-
from django.shortcuts import HttpResponse, render, render_to_response
from django.http import StreamingHttpResponse
from django.template import RequestContext, loader
from models import *
from utils import *
from unicodecsv import writer
from django.conf import settings
from django.template.loader import get_template
from django.utils.html import escape
from django.template.context import Context

import os
import StringIO

from xhtml2pdf import pisa


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

	t = loader.get_template("exported_table.html")

	c = RequestContext(request)
	c['persons'] = rs
	c['number_of_records'] = 0

	return HttpResponse(t.render(c))

def list_orders_from_to(request, from_record, howmany):
	"""
	Restitusce lo stesso template di list_all_orders
	ma permette di filtrare i risultati
	"""
	# todo: bug: i record restituiti sono il doppio di howmany poichè la ricerca è fatta sia in Person che in VirtualPerson
	records = csv_records_iterator(howmany, from_record)
	
	person_count = (Person.objects.all()[from_record:howmany]).count() 
	virtual_person_count = (VirtualPerson.objects.all()[from_record:howmany]).count()
	total_count = person_count + virtual_person_count

	t = loader.get_template("exported_table.html")
	
	c = RequestContext(request)
	c['persons'] = records
	c['number_of_records'] = total_count
	c['frm'] = from_record
	c['to'] = howmany
	
	return HttpResponse(t.render(c))

def list_orders_filtered(request):
	found_filter = False
	for f in ['codice', 'unit', 'tipo-codice']:
		if f in request.GET:
			records = all_csv_records_iterator(f, request.GET[f])
			found_filter = True
			break

	if not found_filter:
		records = []

	total_count = 0

	t = loader.get_template("exported_table.html")
	
	c = RequestContext(request)
	c['persons'] = records
	c['number_of_records'] = total_count
	c['frm'] = 0
	c['to'] = 0
	
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
			tipo_codice,
			to_meal, 
			from_meal,
			to_day,
			from_day,
			std_meal
		FROM meal_provision_person
		GROUP BY to_meal, from_meal,to_day,from_day,std_meal,tipo_codice''')

	vs = Person.objects.raw('''SELECT 
			id,COUNT(id) AS pcount, 
			to_meal, 
			from_meal,
			to_day,
			from_day,
			std_meal
		FROM meal_provision_virtualperson
		GROUP BY to_meal, from_meal,to_day,from_day,std_meal''')

	sums_std = list((0 for i in range(0,30)))
	virt_sums_std = list((0 for i in range(0,30)))
	diff_std = list((0 for i in range(0,30)))

	day_three_times = []
	for i in range(0,30):
		day_three_times.append((i/3)+4)

	ll = ['Colazione', 'Pranzo', 'Cena']
	meals = []
	for i in range(0,30):
		meals.append(ll[i%3])

	for p in ps:

		first_meal = meal_number(p.from_day, p.from_meal)
		last_meal = meal_number(p.to_day, p.to_meal)

		for i in range(first_meal, last_meal +1):
			if p.tipo_codice[:2] == 'RS' and i == meal_number(6,1):
				continue

			sums_std[i] += int(p.pcount)

	for v in vs:
		first_meal = meal_number(v.from_day, v.from_meal)
		last_meal = meal_number(v.to_day, v.to_meal)

		for i in range(first_meal, min(last_meal +1, 29)):
			virt_sums_std[i] += int(v.pcount)

	for i in range(0,30):
		diff_std[i] = ORDERED_MEALS_STD[i] - (sums_std[i] + virt_sums_std[i])

	t = loader.get_template("day_sums.html")
	c = RequestContext(request)
	c['std'] = zip(
		day_three_times,
		meals,
		sums_std,
		virt_sums_std, 
		ORDERED_MEALS_STD, 
		diff_std
	)
	return HttpResponse(t.render(c))

def show_assignement():
	# todo: mostra assegnamento generato
	return HttpResponse("Assegnamento generato")

def new_assignement():
	# todo: trigger nuovo assegnamento
	return HttpResponse("Generato nuovo assegnamento. Visualizzalo")


def pdf_report(request, quartier, storeroom, stock):
    '''
    Restituisce un file PDF con una tabella che riepiloga tutti i clan 
    assegnati ad ogni magazzino e ad ogni punto di distribizione
    '''
    
    units = Unit.objects.filter(quartier__number=quartier, storeroom__number=storeroom, stock__letter=stock)

    context = {}

    context['units'] = units
    context['quartier'] = quartier
    context['storeroom'] = storeroom
    context['stock'] = stock
    context['howmany'] = units.count()
    
    context = Context(context)

    template = get_template('pdf.html')
    html = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")),
                                            dest=result,
                                            encoding='UTF-8')
    if not pdf.err:

        filename = 'meal_report_'+quartier+'_'+storeroom+'_'+stock+'.pdf'

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="'+filename+'"'
        response.write(result.getvalue())
        return response

    return HttpResponse('Errore durante la generazione del PDF<pre>%s</pre>' % escape(html))

