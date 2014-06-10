#-*- coding: utf-8 -*-
from django.shortcuts import HttpResponse, render
from django.http import StreamingHttpResponse
from django.template import RequestContext, loader
from models import *
from utils import *
from unicodecsv import writer

def index(request):
	return HttpResponse("<h1>Programma pasti</h1>")

def list_stocks(request):
	ss = Stock.objects.all()
	print(len(ss))
	res = []
	for s in ss:
		res.append(s.__unicode__() + "<br>\n")
	print(res)
	return HttpResponse("<b>Stocks</b><br>" + "".join(res))

def list_all_orders(request):
	rs = all_csv_records_iterator()
	l = len(rs)
	t = loader.get_template("exported_table.html")
	c = RequestContext(request)
	c['persons'] = rs
	c['number_of_records'] = l - 1
	return HttpResponse(t.render(c))

def list_orders_from_to(request, from_d, to_d):
	rs = csv_records_iterator(to_d)
	l = (Person.objects.all()[:to_d]).count() + (VirtualPerson.objects.all()[:to_d]).count()
	t = loader.get_template("exported_table.html")
	c = RequestContext(request)
	c['persons'] = rs
	c['number_of_records'] = l
	c['frm'] = from_d
	c['to'] = to_d
	return HttpResponse(t.render(c))

def list_vpeople(request):
	vv = VirtualPerson.objects.all(to_camst=True)
	mm = []
	for v in vv:
		en = enumerate_meals( v.from_day, v.to_day, v.from_meal, v.to_meal)
		ms = print_meals(v.std_meal, v.col, en)
		rec = make_csv_record(v.as_map())
		rec.extend(ms)
		mm.append(v.as_list())
	t = loader.get_template("vpeople_table.html")
	c = RequestContext(request)
	c['persons'] = mm
	c['number_of_records'] = len(rs)
	return HttpResponse(t.render(c))

def all_orders_to_csv_iterator_writer(request):
	pseudo = Echo()
	w = writer(pseudo)
	response = StreamingHttpResponse(
			(w.writerow(row) for row in all_csv_records_iterator()),
			content_type="text/csv"
		)
	response['Content-Disposition'] = 'attachment; filename="RN2014-Pasti.csv"'
	return response

def orders_to_csv_iterator_writer(request,frm,to):
	print("router works")
	pseudo = Echo()
	w = writer(pseudo)
	response = StreamingHttpResponse(
			(w.writerow(row) for row in csv_records_iterator(to)),
			content_type="text/csv"
		)
	response['Content-Disposition'] = 'attachment; filename="RN2014-Pasti.csv"'
	return response

def show_assignement():
	return HttpResponse("Assegnamento generato")

def new_assignement():
	return HttpResponse("Generato nuovo assegnamento. Visualizzalo")



