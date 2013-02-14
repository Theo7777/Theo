# Create your views here.
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from user_reg.forms import RegistrationForm, LoginForm, Upload
from user_reg.models import Fresher
from django.contrib.auth import authenticate, login, logout
from django.forms import ModelForm
from mysite1.settings import MEDIA_URL, MEDIA_ROOT
from PIL import Image as PImage
from os.path import join as pjoin
from django.http import HttpResponse
#from django.core.files import requests 
#from django.core.files.temp import File 
#from django.conf import NamedTemporaryFile 


def FresherRegistration(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/profile')
	if request.method== 'POST':
	#takes registration form and fills it out with whatever
	#has been posted
		form = RegistrationForm(request.POST)
		if form.is_valid(): #this function checks if the password/username is valid
			user = User.objects.create_user(username=form.cleaned_data['username'],email = form.cleaned_data['email'],password = form.cleaned_data['password'])
			#this ensures that all data comes back clean 
			user.save() #saves user object
			#user_reg creates a new object with all the extra data that the create user can't give
			user_reg = Fresher(user=user, name= form.cleaned_data['name'], birthday= form.cleaned_data['birthday'])
			user_reg.save()
			return HttpResponseRedirect('/profile')
		else:
			#this is if something goes wrong, is incorrect. Redirect back 
			#to the register page with the form
			return	HttpResponse('form error')
			#return render_to_response('register.html', {'form':form}, context_instance= RequestContext(request))			
	else: 
		'''user is not submitting the form, show them a blank registration form'''
		form = RegistrationForm()
		context = {'form':form}
		return render_to_response('register.html', context, context_instance = RequestContext(request))


#this decorator says if the request is not logged in, send them to the log in page we defined in settings, then bring them back here


def LoginRequest(request):
	#always name the function as login request as there is already a built
	#in function called login and will messs up if you do that
	if request.user.is_authenticated():
		return HttpResponseRedirect('/profile')
	elif request.method=='POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username=form.cleaned_data['username']
			password = form.cleaned_data['password']
			user_reg = authenticate(username=username, password = password)
			if user_reg is not None:
				login(request, user_reg)
				return HttpResponseRedirect('/profile')
			else:
				return render_to_response('login.html', {'form':form}, context_instance=RequestContext(request))
		else:
			return render_to_response('login.html', {'form':form}, context_instance=RequestContext(request))

	else:
		'''user is not submitting the form, show the login form'''
		form = LoginForm()
		context = {'form':form}
		return render_to_response('login.html', context, context_instance=RequestContext(request))

def LogoutRequest(request):
	logout(request)
	return HttpResponseRedirect('/home')


@login_required
def Profile(request):
		#if not logged in, we send them to the log in page
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')
	#we get the profile and save it to user_reg. We then send user_reg to the template to call. Can call details from the profile from here
	user_reg = request.user.get_profile()
	'''Saving the profile pic'''
	if request.method =="POST":
		picture_form = Upload(request.POST, request.FILES, instance = user_reg)
		if picture_form.is_valid():
			#avatar = picture_form.cleaned_data['avatar']
			picture_form.save()
			#resize and save image under same filename
			image_file = pjoin(MEDIA_ROOT, user_reg.avatar.name)
			image = PImage.open(image_file)
			image.save(image_file, "JPEG")

			#return HttpResponse('Thanks for uploading the image')#just to test if the image is valid
		#else:
			#return HttpResponse('Fail')#just to test if the image is not valid
	else:
		picture_form = Upload(instance = user_reg)

	if user_reg.avatar:
		image = "/media/" + user_reg.avatar.name
	context = {"user_reg" : user_reg, "picture_form" : picture_form, "image":image, "media_url": MEDIA_URL}
	return render_to_response("profile.html", context, context_instance= RequestContext(request))

def save_file(file, path =''):
	'''Save file function'''
	filename = file._get_name()
	fd = open("%s/ %s" % (MEDIA_ROOT, str(path) + str(filename)), 'wb')
	for chunk in file.chunks():
		fd.write(chunk)
	fd.close()


def Home(request):
	return render_to_response('main.html', context_instance=RequestContext(request))

def Theo(request):
	return render_to_response('parallax.html', context_instance = RequestContext(request))	


'''For my own knowledge:
When the user enters the profile page, because login is required the user is then sent to the login request function. 
This then tests if the user is authenticated. If so, the user is sent to the profile page, if not, the form- using the 
LoginForm created in the form is brought up for the user. If the form is valid then the data that the user inputted is 
then cleaned(Not sure of what this profile does so far) the user is then logged in useing the django
function 'login' which takes a request and the user_reg(Not entirely sure is this is the user or the view/app). 
If not correct then the user is sent to the login page once more, with the data they inputted already there. 
Profile- The user is then allowed to go through the function Profile:
Here there is a check if the user is authenticated, I then get the user information by calling request.user.get_profile(). I 
set user to None. I then check if the request method was a "POST" and then I, in the same way as loginrequest'''

'''For my own knowledge forms- below I am creating a form  and then testing to see if the form
		is valid. In my models, the user has a one to one field relationship with User.
		User already has object properties of username, email, password etc. so I create a "user" from the.create_user() function
		I then save the data as user using save(). I then instantiate(create a new instance) a new object called user_reg
		whiich uses the data from that user and adds on the fields from the Fresher class. So I add on name, birthday etc.
		It is important, however, that I use "user=user" to show it is the same user. I then save the new object. 
		Going forward I use the user_reg object to describe the user's  information. In the settings.get profile, user_reg
		is the user.get_profile. So I always get birthday and name as well. When I want to send to the template
		I still send user_reg before I render the "Profile". So when I call user_reg in the template I am able to chose
		from all of the data in user_reg'''




