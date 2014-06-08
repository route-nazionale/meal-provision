from meal_provision.models.stock import *
from meal_provision.models.clanfuoco import *
from globals import *

def populate_quartiers():
	for q in QUARTIERS:
		oq = Quartier.objects.filter(color=q)
		if not oq:
			nq = Quartier(
				number=q[0],
				color=q[1],
				storerooms_number=q[2]
				)
			nq.save()
			for j in range(1,q[2]+1):
				ns = Storeroom(quartier=nq, number=j)
				ns.save()
				for k in range(1, q[3]+1):
					nstock = Stock(
						letter=STOCK_LETTERS[k-1], 
						box_number=0,
						storeroom=ns,
						quartier=nq
					)
					nstock.save()

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