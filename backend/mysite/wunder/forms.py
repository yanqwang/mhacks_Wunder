from django import forms

class SearchForm(forms.Form):
	name = forms.CharField(label='Name', max_length=100)
	gender = forms.ChoiceField(label='Gender', choices=[(1,'male'),(2,'female')])
	age = forms.CharField(label='Age', max_length=100)
	language = forms.CharField(label='Language', max_length=100)
	active = forms.ChoiceField(label='Active level', choices=[(1,'low'),(2,'medium'),(3,'high')])
	region = forms.CharField(label='Region', max_length=100)

	location = forms.CharField(label='Location', max_length=100)
	duration = forms.CharField(label='Duration', max_length=100)
	style = forms.ChoiceField(label='Style', choices=[(1,"culture"),(2,"outdoor"),(3,"shopping"),(4,"relaxing")])
	season = forms.ChoiceField(label='Season', choices=[(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)])
	budget = forms.ChoiceField(label='Budget', choices=[(1,"$"),(2,"$$"),(3,"$$$")])