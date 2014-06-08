ROUTE_START_DAY=4
ROUTE_END_DAY=13

QUARTIERS = [ 
	# quartier id, color, nr storerooms, nr stocks
	(1, 'arancio', 5, 22),
	(2, 'azzurro', 5, 22),
	(3, 'viola', 5, 22),
	(4, 'verde', 5, 22),
	(5, 'giallo', 5,22),
	(6, 'oneteam', 1, 1),
	(7, 'kinder', 1, 1)
]

NON_RS_UNITS = [
	('oneteam', 'ONETEAM', 'onteam'),
	('kinder', 'ASILO', 'kinder')
]

STOCK_LETTERS = 'A,B,C,D,E,F,G,H,I,J,L,M,N,O,P,Q,R,S,T,U,V,Z'.split(',')

route_days = range(ROUTE_START_DAY, ROUTE_END_DAY + 1)
meals_types = range(0,3)

# number of meals in route
all_meals = range(0,len(route_days) * len(meals_types) + 1)
