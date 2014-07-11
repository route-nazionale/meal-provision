from meal_provision.models.order import *
import sys
import fileinput

codes = [
	105140,
	1094665,
	1094666,
	1099414,
	1099416,
	1123912,
	1128914,
	1167127,
	1189329,
	1219513,
	1291454,
	1309894,
	1332438,
	135587,
	14041,
	157526,
	162261,
	180857,
	208338,
	216272,
	218231,
	223659,
	223979,
	224911,
	261883,
	308539,
	325940,
	34017,
	35066,
	351762,
	355545,
	35599,
	369304,
	392176,
	422060,
	436154,
	450807,
	458727,
	468248,
	499330,
	511557,
	520757,
	521265,
	52615,
	559638,
	588879,
	632430,
	665485,
	676463,
	681364,
	685839,
	685899,
	741270,
	825295,
	848506,
	890474,
	976463,
	976474,
	]

def locateParent(search=[]):
	people_not_found = []
	a_not_found = []

	if len(search) == 0:
		cs = codes
	else:
		cs = search

	for c in cs:
		p = Person.objects.filter(code=str(c)).prefetch_related("unit").first()
		if p == None:
			people_not_found.append(c)
			continue
		a = StockAssignement.objects.filter(unit=p.unit).prefetch_related("stock").first()
		if a == None:
			a_not_found.append(p.code)
			continue
		print("{},{},{},{}".format(p.code, p.unit.quartier, p.unit.storeroom.number, a.stock.letter))

	print("\n\n People not found")
	print(people_not_found)
	print("---")
	print(a_not_found)


