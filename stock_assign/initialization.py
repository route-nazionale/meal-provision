#-*- coding: utf-8 -*-	
from meal_provision.models.stock import *
from meal_provision.models.clanfuoco import *
from globals import *

def populate_quartiers():
	"""
	Popola le tabelle quartier, storeroom e stock
	Le informazioni sul popolamento (QUARTIERS e STOCK_LETTERS)
	sono prese dal modulo globals
	"""

	# Il numero identificicativo dei magazzini è
	# dato da un'enumerazione unica su tutti i magazzini
	# Da 1 a 27
	storeroom_idx = 1

	for q_idx, q_color, q_store_num, q_stock_num in QUARTIERS:

		stock_idx = 0
		oq = Quartier.objects.filter(number=q_idx)

		if not oq:
			nq = Quartier(
				number=q_idx,
				color=q_color,
				storerooms_number=q_store_num
				)
			nq.save()
			populate_stores_and_stocks(storeroom_idx)
			storeroom_idx += q_store_num


def rebuild_store_and_stocks():
	"""
	Ricostruisce le tabelle storeroom e stock (si assume siano vuote)
	a partire da una tabella quartier già popolata, utilizzando
	le informazioni scritte in globals.py
	"""
	store_idx = 1
	for	quartier in QUARTIERS:
		q = (Quartier.objects.filter(number=quartier[0])).first()
		populate_stores_and_stocks(q, store_idx, quartier[3])
		store_idx += q.storerooms_number

def populate_stores_and_stocks (q, initial_store_idx, stocks_num):
	"""
	Costruisce i magazzini (storeroom) e i punti di distribuzione (stock)
	per un quartiere
	"""
	storeroom_idx = initial_store_idx
	stock_idx = 0
	for j in range(1, q.storerooms_number + 1):
		ns = Storeroom(quartier=q, number=storeroom_idx)
		ns.save()
		storeroom_idx += 1

		for k in range(1, int(stocks_num / q.storerooms_number) + 1 ):
			nstock = Stock(
				letter=STOCK_LETTERS[stock_idx],
				box_number=0,
				storeroom=ns,
				quartier=q
			)
			nstock.save()
			stock_idx += 1


def add_unit(vc, vcid, gid, uid='T1'):
	u = Unit.objects.filter(vclan=vc)	
	if u:
		return
	otq = Quartier.objects.filter(color=vc)
	ots = Storeroom.objects.filter(quartier=otq.first())
	otstock = Stock.objects.filter(quartier=otq.first())
	nu = Unit(
		vclan=vc, 
		vclanID=vcid, 
		unitaID=uid, 
		gruppoID=gid,
		quartier=otq.first(),
		storeroom=ots.first(),
		stock=otstock.first()
	)
	nu.save()

def add_non_rs_units():
	for nrs in NON_RS_UNITS:
		if len(nrs) > 2:
			add_unit(nrs[0], nrs[1], nrs[2])
		else:
			add_unit(nrs[0], nrs[1])

def populate_db():
	populate_quartiers()
	add_non_rs_units()

if __name__ == '__main__':
	populate_db()