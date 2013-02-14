from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
#passes model to form and automatically creates form in model
from user_reg.models import Fresher


class RegistrationForm(ModelForm):
	username = forms.CharField(label = (u'User Name'))
	email = forms.EmailField(label=(u'Email Address'))
	password = forms.CharField(label=(u'Password'),widget=forms.PasswordInput(render_value=False))
#the widget- render_value makes a password field and hides it
	password1 = forms.CharField(label=(u'Verify Password'), widget= forms.PasswordInput(render_value=False))

	class Meta:
		model = Fresher
		exclude = ('user',) 

#the above(in meta) excludes the user field so that the model does create the form field for us
	
	def clean_username(self):
		username = self.cleaned_data['username']
	#this is data that comes back from the form after it is passed back from the view. We then add this
	#to the variable username

	#Below we are going to check if the username has already been submitted. Firstly we are going to 
	#try -using try- to see if the username exists by checking the User class in the database whether the
	#username exists. Returns True if it does. However we are looking for a no. So we then go to 
	#User.DoesNotExist to check. If it does not exist, we return the username. If we the try does not work, 
	# we raise the validation error and say that the username already exists
		try:
			User.objects.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError('That username is already taken. Please select another')

	#We are cleaning the password data here in the same way we did with the username. Clean the data
	#that came back from the views
	def clean(self):
		if self.cleaned_data['password'] != self.cleaned_data['password1']:
			raise forms.ValidationError('The passwords do not match. Please try again')
		return self.cleaned_data

		

class Upload(ModelForm):
	class Meta: 
		model = Fresher
		exclude = ('user, birthday, name, image, album')
		




class LoginForm(forms.Form):
	username = forms.CharField(label=(u'User Name'))
	password = forms.CharField(label=(u'Password'), widget = forms.PasswordInput(render_value=False))




