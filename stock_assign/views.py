from django.shortcuts import HttpResponse, render
from django.template import RequestContext, loader
from models import *
from utils import *
from csv import writer

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
	rs = make_all_records()
	l = len(rs)
	t = loader.get_template("exported_table.html")
	c = RequestContext(request)
	c['persons'] = rs
	c['number_of_records'] = l - 1
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

def orders_to_csv(request):
	filename = "Rn2014-Pasti.csv"
	response = HttpResponse(content_type='text_csv')
	response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

	w = writer(response)
	## Write columns titles
	w.writerow(make_csv_titles())
	
	for r in make_all_records():
		w.writerow(r)

	# todo: fai copia cache del file ?


	return response

def show_assignement():
	return HttpResponse("Assegnamento generato")

def new_assignement():
	return HttpResponse("Generato nuovo assegnamento. Visualizzalo")



