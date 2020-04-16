from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from .forms import SignUpForm, EditProfileForm


def home(request):
	import json
	import requests

	if request.method == "POST":
		zipcode = request.POST['zipcode']
		api_request = requests.get("http://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode="+ zipcode + "&distance=5&API_KEY=0371F1AB-2B81-4348-B299-4F618F929FCA")

		try:
			api = json.loads(api_request.content)
		except Exception as e:
			api = "Error..."

		if api[0]['Category']['Name'] == "Good": 
			category_description = "(0-50): Air quality is considered satisfactory, and air pollution poses little or no risk."
			category_color ="good"

		elif api[0]['Category']['Name'] == "Moderate": 
		  	category_description = "(51-100): Air quality is acceptable; however, for some pollutants there may be a moderate health concern for a very small number of people who are unusually sensitive to air pollution."
		  	category_color ="moderate"

		elif api[0]['Category']['Name'] == "Unhealthy for Sensitive Groups": 
		  	category_description = "(101-150): Although general public is not likely to be affected at this AQI range, people with lung disease, older adults and children are at a greater risk from exposure to ozone, whereas persons with heart and lung disease, older adults and children are at greater risk from the presence of particles in the air."
		  	category_color ="unhealthyforsensitivegroups"

		elif api[0]['Category']['Name'] == "Unhealthy": 
		  	category_description = "(151-200):Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects."
		  	category_color ="unhealthy"

		elif api[0]['Category']['Name'] == "Very unhealthy":
		  	category_description = "(201-300):Health alert, everyone may experience more serious health effects."
		  	category_color = "veryunhealthy"


		elif api[0]['Category']['Name'] == "Hazardous":
		  	category_description = "(301-500):Health warnings of emergency conditions. The entire population is more likely to be affected."
		  	category_color ="hazardous"

		return render(request, 'home.html', {
			'api': api, 
			'category_description': category_description, 
			'category_color': category_color})
	else:
		api_request = requests.get("http://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=11210&distance=5&API_KEY=0371F1AB-2B81-4348-B299-4F618F929FCA")

		try:
			api = json.loads(api_request.content)
		except Exception as e:
			api = "Error..."

		if api[0]['Category']['Name'] == "Good": 
			category_description = "(0-50): Air quality is considered satisfactory, and air pollution poses little or no risk."
			category_color ="good"
		elif api[0]['Category']['Name'] == "Moderate": 
		  	category_description = "(51-100): Air quality is acceptable; however, for some pollutants there may be a moderate health concern for a very small number of people who are unusually sensitive to air pollution."
		  	category_color="moderate"

		elif api[0]['Category']['Name'] == "Unhealthy for Sensitive Groups": 
		  	category_description = "(101-150): Although general public is not likely to be affected at this AQI range, people with lung disease, older adults and children are at a greater risk from exposure to ozone, whereas persons with heart and lung disease, older adults and children are at greater risk from the presence of particles in the air."
		  	category_color="unhealthyforsensitivegroups"

		elif api[0]['Category']['Name'] == "Unhealthy": 
		  	category_description = "(151-200):Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects."
		  	category_color ="unhealthy"

		elif api[0]['Category']['Name'] == "Very unhealthy":
		  	category_description = "(201-300):Health alert, everyone may experience more serious health effects."
		  	category_color = "veryunhealthy"


		elif api[0]['Category']['Name'] == "Hazardous":
		  	category_description = "(301-500):Health warnings of emergency conditions. The entire population is more likely to be affected."
		  	category_color ="hazardous"

		return render(request, 'home.html', {
			'api': api, 
			'category_description': category_description, 
			'category_color': category_color})

def about(request):
	return render(request, 'about.html', {})

def login_user(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ('You Have Been Logged in!'))
			return redirect('welcome')
		else:
			messages.success(request, ('Error Logged in - Please Try Again!'))
			return redirect('login')
	else:
		return render(request, 'login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request, ('You Have Been Logged out Successfully!'))
	return redirect('welcome')

def welcome(request):
	return render(request, 'welcome.html', {})

def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ('You Have Been Successfully Registered!'))
			return redirect('welcome')

	else:
		form = SignUpForm()

	context = {'form': form}
	return render(request, 'register.html', context)

def edit_profile(request):
	if request.method == 'POST':
		form = EditProfileForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, ('You Have Edited Your Profile!'))
			return redirect('welcome')

	else:
		form = EditProfileForm(instance=request.user)

	context = {'form': form}
	return render(request, 'edit_profile.html', context)

def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(data=request.POST, user=request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, ('You Have Changed Your Password!'))
			return redirect('welcome')

	else:
		form = PasswordChangeForm(user=request.user)

	context = {'form': form}
	return render(request, 'change_password.html', context)
