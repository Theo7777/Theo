from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from images.models import Image, Album
# Create your models here.

class Fresher(models.Model):
	user = models.OneToOneField(User, unique = True)
	birthday = models.DateField(null=True)
	name = models.CharField(max_length=100)
	image = models.ManyToManyField(Image)
	album = models.ManyToManyField(Album)
	avatar = models.ImageField("Profile Pic", upload_to='images/', blank =True, null=True)

	def __unicode__(self):
		return unicode (self.user)

#This model is what is shown to the user when they log in. We could also use some of the details from the form in form.py 
#such as email, password etc. It creates a section called User_reg where I get all the details from Fresher
#create our user object to attach to our fresher object
#def create_fresher_user_callback(sender, instance, **kwargs):
#new returns true if the user is new(created) or false is already exists(get)	
#	fresher, new = Fresher.objects.get_or_create(user=instance)
#any time user object created, this registers post save
#post_save.connect(create_fresher_user_callback, User) 


