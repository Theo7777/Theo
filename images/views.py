# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.forms import ModelForm
from mysite1.settings import MEDIA_URL, MEDIA_ROOT
from images.forms import ImageForm
import os
from os.path import join as pjoin
from PIL import Image as PImage
from os.path import join as pjoin


from images.models import *

def main(request):
	'''Main Listing.'''
	#get all albums from the db
	albums = Album.objects.all()
	#check is the user is authenticated to see whether to direct to public/private images
	#if not, send them only to public directory
	if not request.user.is_authenticated():
		albums = albums.filter(public=True)

	#Use the paginator to show 10 albums. Then check for errors
	paginator = Paginator(albums, 10)
	try: page = int(request.GET.get("page", '1'))
	except ValueError: page = 1

	try:	
		albums = paginator.page(page)
	except (InvalidPage, EmptyPage):
		albums = paginator.page(paginator.num_pages) 

	#Iterate through the albums and them list all the albums. However, 
	#only how the first 4 images in the albums

	for album in albums.object_list:
		album.images = album.image_set.all()[:4]

	#load up the template- photo/list.html, create a dictionary
	#send over album as album, user is the user who requested
	#my media_url is my MEDIA_URL

	return render_to_response("list.html", dict(albums=albums, user=request.user,
        media_url=MEDIA_URL), context_instance = RequestContext(request))

'''This function is used to create individual pages for albums'''
def album(request, pk):
	'''album listing'''
	#get the primary key for the album
	album = Album.objects.get(pk=pk)
	#check if the album is public and if user is authenticated
	if not album.public and not request.user.is_authenticated():
		return HttpResponse("Error: you need to be logged in to view this album")

	#include the paginator and see if there are multiple pages	
	images = album.image_set.all()
	paginator = Paginator(images, 30)
	try: page = int(request.GET.get("page", '1'))
	except ValueError: page = 1

	try:
		images = paginator.page(page)
	except (InvalidPage, EmptyPage):
		images = paginator.page(paginator.num_pages)

	#send the user to album, with the dictionary carrying the variables album, images, users,media_url	
	return render_to_response("album.html", dict(album= album, images = images, user= request.user, media_url =MEDIA_URL), 
		context_instance = RequestContext(request))

def image(request, pk):
	'''Image page.'''
	img = Image.objects.get(pk=pk)
	return render_to_response("image.html", dict(image=img, 
		user=request.user, backurl=request.META.get("HTTP_REFERER"), media_url=MEDIA_URL), context_instance=RequestContext(request))



def save_file(file, path=""):
	'''This is the view to save the image file'''
	filename = file._get_name()
	fd = open('%s/%s' % (MEDIA_ROOT, str(path) + 'images/' +str(filename)), 'wb')
	for chunk in file.chunks():
		fd.write(chunk)
	fd.close()


@login_required
def ImageInsert(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')
	profile = request.user.get_profile()

	'''saving the pic'''
	if request.method =="POST":
		image_form = ImageForm(request.POST, request.FILES, instance = profile)
		if image_form.is_valid():
			image_form.save()
			#resize and save image under same filename
			image_file = pjoin(MEDIA_ROOT, user_reg.avatar.name)
			image = PImage.open(image_file)
			image.save(image_file, "JPEG") 
	else:
		image_form = ImageForm(instance = profile)

	if profile.image:
		image = "/media/" + profile.image.name
	
	context = {"profile" : profile, "image_form" : image_form, "image":image, "media_url": MEDIA_URL}
	return render_to_response("upload.html", context, context_instance= RequestContext(request))















