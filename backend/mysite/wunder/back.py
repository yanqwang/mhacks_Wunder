class DataEntry:
	def __init__(self, profile, itinerary, match=0):
		self.profile = profile
		self.itinerary = itinerary
		self.match = match

class Database:

	def __init__(self):
		self.Data = list()

	def add(self, profile, itinerary):
		self.Data.append(DataEntry(profile, itinerary))

	def search(self, profile, tripnode):
		rst = list()
		for entry in self.Data:
			if (entry.itinerary.match(tripnode)):
				match = profile.match_profile(entry.profile)
				d = DataEntry(entry.profile, entry.itinerary, match=match)
				rst.append(d)
		rst.sort(key=lambda x: x.match, reverse=True)
		for i in range(len(rst)):
			entry = rst[i]
			print(entry.match)

			for j in range(len(entry.itinerary.tripnodes)):
				trip_node = entry.itinerary.tripnodes[j]
				print(trip_node.location, end=' ')
			print('\n')
		return rst

class Profile:
	# gender: text "male" or "female"
	# age: int
	# lang: text "Chinese",...,"English"
	# active: text "low", "medium", "high"
	# region: text
	def __init__(self,gender,age,lang,active,region):
		self.gender = gender
		self.age = age
		self.lang = lang
		self.active = active
		self.region = region

	def age_range(self):
		# 0-12: 1
		# 12-30:2
		# 30-50:3
		# 50-**:4
		if (self.age < 12):
			return 0
		elif (self.age < 30):
			return 1
		elif (self.age < 50):
			return 2
		else:
			return 3

	def match_profile(self, other_profile):
		count = 0
		if (other_profile.gender == self.gender):
			count += 1
		if (other_profile.lang == self.lang):
			count += 1
		if (other_profile.active == self.active):
			count += 1
		if (other_profile.region == self.region):
			count += 1
		if (other_profile.age_range() == self.age_range()):
			count += 1
		return count

class TripNode:
	# location: text
	# season: int 1-12
	# budget: int $,$$,$$$
	# duration: int in days
	# style: text, int "culture","outdoor","shopping","relaxing"
	# optional
	# description: text optional description of trip node
	# image: 2D array optional image of trip node

	def __init__(self, loc=None, season=None, budget=None, dur=None, sty=None):
		self.location = loc
		self.season = season
		self.budget = budget
		self.duration = dur
		self.style = sty
		self.description = ""
		self.image = None

	def match_TripNode(self, other_tripnode):
		# other_tripnode must have complete information
		if (self.location != None):
			if (self.location != other_tripnode.location):
				return False
		
		if (self.season != None):
			if ((not (self.season == 1 and other_tripnode.season == 12)) \
					and (not (self.season == 12 and other_tripnode.season == 1)) \
					and (self.season < other_tripnode.season-1 or self.season > other_tripnode.season+1) ):
				return False
		
		
		if (self.duration != None):
			if (self.duration < other_tripnode.duration-1 or self.duration > other_tripnode.duration+1):
				return False

		return True
		
class Itinerary:
	# start_loc: text
	# tripnodes: list of TripNode
	def __init__(self, start_loc):
		self.start_loc = start_loc
		self.tripnodes = list()
		self.length = 0

	def add(self, tripnode):
		self.tripnodes.append(tripnode)
	
	def length(self):
		return len(self.tripnodes)

	def match(self, trip_node):
		for node in self.tripnodes:
			if (trip_node.match_TripNode(node)):
				return True;
		return False

	def print_nodes(self):
		for t in self.tripnodes:
			print(t.location, end=' ')
			print(t.style, end=' ')
			print('')


if __name__ == "__main__":
	db = Database()
	node1 = TripNode("Shanghai",1,'$',3,"relaxing")
	node2 = TripNode("Beijing", 1, '$$',2,"shopping")
	it1 = Itinerary("Home")
	it1.add(node1)
	it1.add(node2)
	it1.print_nodes()

	print('')

	node3 = TripNode("Shanghai",12,'$',2,"culture")
	node4 = TripNode("Hefei", 2, '$', 4,"outdoor")
	it2 = Itinerary("Jiaxin")
	it2.add(node3)
	it2.add(node4)
	it2.print_nodes()


	tp1 = TripNode("Shanghai", 1, '$$$', 2, "relaxing")
	tp2 = TripNode("Beijing", 2, '$',3, "outdoor")

	print(tp1.match_TripNode(node1))
	print(tp1.match_TripNode(node2))
	print(tp2.match_TripNode(node1))
	print(tp2.match_TripNode(node2))
	print('eee')
	print(it1.match(tp1))
	print(it1.match(tp2))
	print(it2.match(tp1))
	print(it2.match(tp2))

	p = Profile('male', 15,'English','high','North America')
	db.add(p,it1)
	db.add(p,it2)

	p2 = Profile('female', 15,'English','low','North America')
	db.search(p2, node3)