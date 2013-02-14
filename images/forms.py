from django import forms
from django.forms import ModelForm
from images.models import Image
#passes model to form and automatically creates form in model



class ImageForm(ModelForm):
	class Meta:
		model = Image

		exclude = ('title, tags, albums, created, rating, width, height, user')
