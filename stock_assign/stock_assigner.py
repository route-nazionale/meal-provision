import heapq
import random
import time
import math

#: Number of meals contained in a box (defined by caterer)
MEALS_IN_A_BOX = 17

class Stock():
	""" Describes stocks in the heapq"""
	# The containing storeroom (dispensa)
	storeroom = 0

	# Identification letter for the stock (punto di stoccaggio)
	letter = "A"

	# Number of boxes to be contained in this stock
	box_num = 0

	# Number of communities that are served by this stock
	clan_num = 0

	def __init__(self, s, l):
		self.storeroom = s
		self.letter = l

	def __cmp__(self, other):
		return self.box_num > other.box_num

	def add(self, clan):
		self.box_num += clan.boxes_needed
		self.clan_num += 1

class Clan():
	"""Describes clans"""	
	name = ""
	#: How many people are in this clan
	member_num = 0

	#: How many boxes needed by this clan (calculated)
	boxes_needed = 0

	#: Which stock is serving this clan (empty if not assigned)
	stock = ""

	def __init__(self, n, mn):
		self.name = n
		self.member_num = mn
		self.boxes_needed = self.calculate_boxes(mn, MEALS_IN_A_BOX)

	def calculate_boxes(m, n):
		return math.ceil( float(m) / float(n))

	def assign(self, stck):
		self.stock = stck.letter

class StockAssigner():
	"""Class to assign clans to stocks"""
	stock_num = 0
	clan_num = 0

	stocks = []
	clans = []

	def __init__(self, stocklist, clanlist):
		self.clans = sorted(clanlist,reverse=True)
		self.clan_num = len(self.clans)
		self.stocks = stocklist
		heapq.heapify(self.stocks)
		self.stock_num = len(self.stocks)

	def partition(self):
		"""
		The assignement algorithm: just a greedy algorithm that scans
		the list of clans ordered by descending number of boxes and assign
		them to the least crowded stock (good results when boxes_needed have
		low variance w.r.t number of clans)
		"""
		for c in self.clans:
			s = heapq.heappop(self.stocks)
			s.add(c)
			c.assign(s)
			heapq.heappush(self.stocks, s)

	def printout(self):
		print("== STOCKS ==")
		for s in sorted(self.stocks):
			print("{}\t{}\t{}".format(s.letter, int(s.box_num), s.clan_num))

		print("\n== CLANS ==")
		for c in sorted(self.clans, key=lambda c: c.stock):
			print("{}\t\t{}\t{}\t{}".format(c.name, c.member_num, c.boxes_needed, c.stock))

def test():
	storeroom = 1
	CLAN_NUM = 260
	CLAN_MIN_MEMBERS = 5
	CLAN_MAX_MEMBERS = 80

	# create stocks list
	ls = "A,B,C,D,E,F,G,H,I,J,L,M,N,O,P,Q,R,S,T,U,V,Z".split(",")
	sl = []
	for l in ls:
		sl.append(Stock(1, l))

	random.seed(time.time())

	#create a list of CLAN_NUM clans with a random number of members
	# between CLAN_MIN_MEMBERS and CLAN_MAX_MEMBERS
	cl = []
	for i in range(1,CLAN_NUM):
		cl.append(
			Clan(
				"Italia"+`i`,
				random.randint(CLAN_MIN_MEMBERS, CLAN_MAX_MEMBERS)
			)
		)

	sa = StockAssigner(sl, cl)
	sa.partition()
	sa.printout()

