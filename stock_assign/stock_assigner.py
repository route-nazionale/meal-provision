import heapq
import random
import time
import math
from meal_provision.models.clanfuoco import *
from meal_provision.models.stock import *

class StockAssigner():
	"""Class to assign clans to stocks"""
	
	stock_num = 0
	clan_num = 0

	stocks = []
	clans = []

	def __init__(self, r):
		
		print("Cerco il magazzino")

		room = Storeroom.objects.get(pk=r)

		print("Scarico la lista dei clan")

		self.clans = Unit.objects.filter(storeroom=room).order_by("-size")
		
		# self.clan_num = len(self.clans)
		
		print("Scarico la lista degli stoccaggi")
		self.stocks = list(Stock.objects.filter(storeroom=room))

		print("Costruisco la heap")
		heapq.heapify(self.stocks)

		print("Finito")
		
		# self.stock_num = len(self.stocks)

	def partition(self):
		"""
		The assignement algorithm: just a greedy algorithm that scans
		the list of clans ordered by descending number of boxes and assign
		them to the least crowded stock (good results when boxes_needed have
		low variance w.r.t number of clans)
		"""
		for c in self.clans:

			s = heapq.heappop(self.stocks)

			# todo: check that no doubles of the same group are in the stock

			s.add(c.size)
			c.assign(s)
			print("{}\t\t\t{}".format(c.vclan, s.__unicode__()))

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

def init_test2():
	s1 = Storeroom.objects.filter(number=1).first()
	StockAssigner(s1)

def assignAll():
	for i in range(1,28):
		sa = StockAssigner(i)
		sa.partition()