import sqlite3 as sq3 



class DataEntry:
	def __init__(self, profile, itinerary, match=0):
		self.profile = profile
		self.itinerary = itinerary
		self.match = match

class Database:

	def __init__(self):
		self.Data = list()
		self.db_cursor = sq3.connect("db.sqlite3")
		if (self.profile_is_empty()):
			self.create_profile_table()
		if (self.itinerary_is_empty()):
			self.create_itinerary_table()

	def __del__(self):
		self.db_cursor.close()


	def profile_is_empty(self):
		profile_table_exists = len(self.db_cursor.execute("""SELECT name
											FROM sqlite_master
											WHERE type='table' AND name='PROFILE_TABLE'; """).fetchall()) == 0

		return profile_table_exists

	def itinerary_is_empty(self):
		itinerary_table_exists = len(self.db_cursor.execute("""SELECT name
											FROM sqlite_master
											WHERE type='table' AND name='ITINERARY_TABLE'; """).fetchall()) == 0

		return itinerary_table_exists

	def create_profile_table(self):
		self.db_cursor.execute("""
							CREATE TABLE PROFILE_TABLE
							(IID INT PRIMARY KEY NOT NULL,
							GENDER INT NOT NULL,
							AGE INT NOT NULL,
							ACTIVE INT NOT NULL
							);
						""")

	def create_itinerary_table(self):
		self.db_cursor.execute("""
							CREATE TABLE ITINERARY_TABLE
							(ID INT PRIMARY KEY NOT NULL,
							IID INT NOT NULL,
							NID INT NOT NULL,
							LOCATION TEXT NOT NULL,
							SEASON INT NOT NULL,
							DURATION INT NOT NULL,
							BUDGET INT NOT NULL,
							STYLE INT NOT NULL
							);
						""")

	def add_to_table(self, profile, itinerary):
		tail_id_profile = len(self.db_cursor.execute("SELECT IID FROM PROFILE_TABLE").fetchall())
		self.db_cursor.execute("""
							INSERT INTO PROFILE_TABLE (IID, GENDER, AGE, ACTIVE)
							VALUES (%d, %d, %d, %d);"""
							%((tail_id_profile+1), profile.gender, profile.age, profile.active))
		print(tail_id_profile)
		tail_id_itinerary = len(self.db_cursor.execute("SELECT ID FROM ITINERARY_TABLE").fetchall())
		print(tail_id_itinerary)
		for i in range(len(itinerary.tripnodes)):
			temp = itinerary.tripnodes[i]
			self.db_cursor.execute("""
								INSERT INTO ITINERARY_TABLE (ID, IID, NID, LOCATION, SEASON, DURATION, BUDGET, STYLE)
								VALUES (%d, %d, %d, '%s', %d, %d, %d, %d);"""
								%((tail_id_itinerary+i+1), (tail_id_profile+1), (i+1), \
									temp.location, temp.season, temp.duration, temp.budget, temp.style))
		self.db_cursor.commit()

	def load_to_memory(self):
		profile_list = self.db_cursor.execute("""SELECT IID, GENDER, AGE, ACTIVE 
													FROM PROFILE_TABLE
													ORDER BY IID;""").fetchall()

		itinerary_list = self.db_cursor.execute("""SELECT ID, IID, NID, LOCATION, SEASON, DURATION, BUDGET, STYLE
													FROM ITINERARY_TABLE
													ORDER BY IID;""").fetchall()
		profile_list_len = len(profile_list)
		ptr = 0
		for i in range(profile_list_len):
			profile = Profile(profile_list[i][1], profile_list[i][2], 'english', profile_list[i][3], 'us')
			same_iid_list = list()
			while (itinerary_list[ptr] == profile_list[i][0]):
				same_iid_list.append(itinerary_list[ptr])
				ptr += 1
			same_iid_list.sort(key=lambda x: x[2])
			itinerary = Itinerary('home')
			for j in range(len(same_iid_list)):
				tripnode = TripNode(loc=same_iid_list[j][3], season=same_iid_list[j][4], \
				 budget=same_iid_list[j][6], dur=same_iid_list[j][5], sty=same_iid_list[j][7])
				itinerary.add(tripnode)
			self.add(profile, itinerary)
				




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
	# style: int, int "culture","outdoor","shopping","relaxing"
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
	node1 = TripNode("Shanghai",1,1,3,1)
	node2 = TripNode("Beijing", 1,2,2,3)
	it1 = Itinerary("Home")
	it1.add(node1)
	it1.add(node2)
	it1.print_nodes()

	print('')

	node3 = TripNode("Shanghai",12,1,2,3)
	node4 = TripNode("Hefei", 2, 2, 4,1)
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

	# p = Profile('male', 15,'English','high','North America')
	# db.add(p,it1)
	# db.add(p,it2)

	# p2 = Profile('female', 15,'English','low','North America')
	# db.search(p2, node3)

	p1 = Profile(1, 15, 'english', 2, 'us')
	db.add_to_table(p1, it1)
	db.add_to_table(p1, it2)


