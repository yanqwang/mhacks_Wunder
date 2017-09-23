from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import QueryDict
from .forms import SearchForm

from .back import Profile
from .back import TripNode
from .back import Itinerary
from .back import Database

# Create your views here.
budget_dict = {1: '$', 2: '$$', 3:'$$$'}
style_dict = {1: 'culture', 2: 'outdoor', 3: 'shopping', 4: 'relaxing'}

db = Database()
# initialize database data here
# node1 = TripNode("Shanghai",1,'$',3,"relaxing")
# node2 = TripNode("Beijing", 1, '$$',2,"shopping")
node1 = TripNode("Shanghai",1,1,3, 4)
node2 = TripNode("Beijing", 1, 2,2,3)
it1 = Itinerary("Home")
it1.add(node1)
it1.add(node2)
it1.print_nodes()

# node3 = TripNode("Shanghai",12,'$',2,"culture")
# node4 = TripNode("Hefei", 2, '$', 4,"outdoor")
node3 = TripNode("Shanghai",12,1,2,1)
node4 = TripNode("Hefei", 2, 1, 4,2)
it2 = Itinerary("Jiaxin")
it2.add(node3)
it2.add(node4)
it2.print_nodes()

# p = Profile('male', 15,'English','high','North America')
p = Profile(1, 15,'English',3,'North America')
db.add(p,it1)
db.add(p,it2)


def index(request):
    return HttpResponse("Hello world")

def search(request):

	return HttpResponse("Search page")

def upload(request):
	return HttpResponse("Upload page")

def get_search(request):
	if request.method == 'POST':
	# create a form instance and populate it with data from the request:
		form = SearchForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL:
			return HttpResponseRedirect('/thanks/')

	# if a GET (or any other method) we'll create a blank form
	else:
		form = SearchForm().as_p()
	
	return render(request, 'search.html', {'form': form})

def get_upload(request):
	return render(request, 'upload.html')

def upload_recv(request):
	print("enter upload recev")
	print(request.body)
	return render(request, 'search.html')

def search_recv(request):
	print("search result")
	data = QueryDict(request.body)
	print(data)
	profile = Profile(int(data['gender'][0]), int(data['age'][0]), data['language'], int(data['active'][0]),data['region'])
	trip_node = TripNode(data['location'],int(data['season'][0]),int(data['budget'][0]),int(data['duration'][0]),int(data['style'][0]))
	print(int(data['gender'][0]), int(data['age'][0]), data['language'][0], int(data['active'][0]),data['region'][0])
	print(data['location'][0],int(data['season'][0]),int(data['budget'][0]),int(data['duration'][0]),int(data['style'][0]))
	rst = db.search(profile, trip_node)

	html = "<p>666</p>"
	print(len(db.Data))
	print(len(rst))
	for i in range(len(rst)):
		html += " <h2> Attempted Trip "+ str(i) + "</h2>"
		trip = ""
		for j in range(len(rst[i].itinerary.tripnodes)):
			trip += "<h2> Step " + str(j) + "</h2>"
			trip += "<p> Location: "+ rst[0].itinerary.tripnodes[i].location + "</p>"
			trip += "<p> Season: "+ str(rst[0].itinerary.tripnodes[i].season) + "</p>"
			trip += "<p> Duration: "+ str(rst[0].itinerary.tripnodes[i].duration) + "</p>"
			trip += "<p> budget: "+ budget_dict[rst[0].itinerary.tripnodes[i].budget] + "</p>"
			trip += "<p> style: "+ style_dict[rst[0].itinerary.tripnodes[i].style] + "</p>"
		html += trip
	print("test html"+html)
	return render(request, 'search-result.html', {'html': html})