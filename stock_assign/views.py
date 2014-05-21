from django.shortcuts import HttpResponse, render
from models import *

def index(request):
	ss = MyStock.objects.all()
	res = ",".join(ss)
	return HttpResponse("Hello world")