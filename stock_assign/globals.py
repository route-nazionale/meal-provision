#-*- coding: utf-8 -*-
ROUTE_START_DAY=4
ROUTE_END_DAY=13

QUARTIERS = [ 
	# quartier id, color, nr storerooms, nr stocks
	(1, 'arancio', 5, 20),
	(2, 'azzurro', 5, 20),
	(3, 'viola', 5, 20),
	(4, 'verde', 5, 20),
	(5, 'giallo', 5,20),
	(6, 'oneteam', 1, 1),
	(7, 'kinder', 1, 1)
]

NON_RS_UNITS = [
	('oneteam', 'ONETEAM', 'onteam'),
	('kinder', 'ASILO', 'kinder')
]

STOCK_LETTERS = 'A,B,C,D,E,F,G,H,I,L,M,N,O,P,Q,R,S,T,U,V,Z'.split(',')

route_days = range(ROUTE_START_DAY, ROUTE_END_DAY + 1)
meals_types = range(0,3)

# number of meals in route
all_meals = range(0,len(route_days) * len(meals_types))

ORDERED_MEALS_STD = [
	0, 
	1095, 
	1095, 
	1185, 
	1185, 
	1457, 
	1457, 
	1185, 
	29100, 
	29275, 
	29275, 
	29795, 
	29795, 
	30105, 
	29795, 
	29795, 
	30105, 
	29295, 
	29285, 
	29285, 
	16370, 
	565, 
	565, 
	565, 
	535, 
	535, 
	535, 
	475, 
	475, 
	0
]

ORDERED_MEALS_ALTRO = list(( i * 6 / 100 for i in ORDERED_MEALS_STD))