from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import QueryDict
from .forms import SearchForm
from .forms import ProfileForm
from .forms import UploadForm

from .back import Profile
from .back import TripNode
from .back import Itinerary
from .back import Database

import os

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

def get_css(request):
	path = request.path
	name = ""
	if (path.find("style.css")!=-1):
		name = "style.css"
	else:
		name = "materialize.css"
	with open('css/'+name, 'rb') as f:
		css_data = f.read()
	return HttpResponse(css_data, "mimetype='text/css'")

def get_image(request):
	# print(request.path)
	# os.system("pwd")
	# os.system("ls")
	path = request.path
	name = path[path.find("IMG"):]
	image_data = None
	with open('images/'+name, 'rb') as f:
		image_data = f.read()
	return HttpResponse(image_data, "mimetype='image/jpg'")

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
	print("get upload")
	input_str = "<input type='submit' value='Submit' />"
	separate_str = "<p>==============================================</p>"
	if request.method == 'POST':
		form = ProfileForm(request.POST).as_p()
		it_form = UploadForm().as_p()
		print(request.body)
		data = QueryDict(request.body)
		if (int(data['num'][0])==1):
			return render(request, 'upload.html', {'profile_form': form, 'it_form_1': it_form, 'input_str': input_str})
		elif (int(data['num'][0])==2):
			return render(request, 'upload.html', {'profile_form': form, 'it_form_1': it_form, 'separate_1': separate_str, \
														'it_form_2': it_form, 'input_str': input_str})
		else:
			return render(request, 'upload.html', {'profile_form': form, 'it_form_1': it_form, 'separate_1': separate_str, \
														'it_form_2': it_form, 'separate_2': separate_str, \
														'it_form_3': it_form, 'input_str': input_str})
	else:
		form = ProfileForm().as_p()
		return render(request, 'upload.html', {'profile_form': form})

def upload_recv(request):
	print("enter upload recev")
	# print(request.body)
	data = QueryDict(request.body)
	print(data)
	return HttpResponse("hello world")

def search_recv(request):
	print("search result")
	data = QueryDict(request.body)
	print(data)
	profile = Profile(int(data['gender'][0]), int(data['age'][0]), data['language'], int(data['active'][0]),data['region'])
	trip_node = TripNode(data['location'],int(data['season'][0]),int(data['budget'][0]),int(data['duration'][0]),int(data['style'][0]))
	print(int(data['gender'][0]), int(data['age'][0]), data['language'][0], int(data['active'][0]),data['region'][0])
	print(data['location'][0],int(data['season'][0]),int(data['budget'][0]),int(data['duration'][0]),int(data['style'][0]))
	rst = db.search(profile, trip_node)

	html = ""
	print(len(db.Data))
	print(len(rst))
	row_head = "<div class = 'row'>"
	row_end = "</div>"
	col_12_head = "<div class = 'col s12'>"
	col_8_head = "<div class = 'col s8'>"
	col_4_head = "<div class = 'col s4'>"
	col_end = "</div>"
	gray_head = "<div class='text'>"
	gray_end = "</div>"
	for i in range(len(rst)):
		html += " <h2> Attempted Trip "+ str(i) + "</h2>"
		trip = ""
		
		for j in range(len(rst[i].itinerary.tripnodes)):
			trip += "<h3> Step " + str(j) + "</h3>"
			trip += gray_head + row_head
			trip += col_12_head
			content = "<p class='info'> Location: "+ rst[i].itinerary.tripnodes[j].location + "</p>" \
					+ "<p class='info'> Season: "+ str(rst[i].itinerary.tripnodes[j].season) + "</p>" \
					+ "<p class='info'> Duration: "+ str(rst[i].itinerary.tripnodes[j].duration) + "</p>" \
					+ "<p class='info'> budget: "+ budget_dict[rst[i].itinerary.tripnodes[j].budget] + "</p>" \
					+ "<p class='info'> style: "+ style_dict[rst[i].itinerary.tripnodes[j].style] + "</p>"
			trip += col_4_head + content + col_end
			trip += col_8_head 
			trip += row_head
			img_left = "<img src='images/IMG01.JPG'>"
			trip += col_4_head + img_left + col_end
			img_right = "<img src='images/IMG02.JPG'>"
			trip += col_4_head + img_right + col_end
			trip += row_end
			trip += row_head
			text = "Interdum et malesuada fames ac ante ipsum primis in faucibus. Aliquam vulputate ullamcorper magna nec porta. Aenean sed elit felis. Duis efficitur rhoncus imperdiet. Morbi in porta nulla. Suspendisse molestie ante leo, sit amet sodales urna porta euismod. Phasellus nibh ligula, volutpat sit amet sollicitudin ut, lobortis in dui. Praesent ut risus tristique, facilisis nibh ac, eleifend lacus. Nam a est ac turpis fermentum ornare."
			trip += col_8_head + text + col_end
			trip += row_end
			trip += col_end #col_8_end
			trip += col_end #col_12_end
			trip += row_end + gray_end
			
		html += trip
	print("test html"+html)
	return render(request, 'search-result.html', {'html': html})