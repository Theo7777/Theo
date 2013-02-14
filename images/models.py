from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

from string import join
import os 
from PIL import Image as PImage
from mysite1.settings import MEDIA_ROOT
#This is added from the generating thumbnails section
from django.core.files import File
from os.path import join as pjoin
from tempfile import *



'''Here I'm creating an album class with a title, max_length=60,and creating a
section checking whether the album is public or not. This is set to False
by default'''
class Album(models.Model):
        title = models.CharField(max_length = 60)
        public= models.BooleanField(default= False)

        def __unicode__(self):
                return self.title
        '''Here we're adding a list of links to images in the Album listing 
         the image set object is automatically created as part of the many to many relationship'''
        def images(self):
            lst = [x.image.name for x in self.image_set.all()]
            lst = ["<a href='/media/%s'>%s</a>" % (x, x.split('/')[-1]) for x in lst]
            return join(lst,', ')

        images.allow_tags = True

'''Here I'm creating a tag class which creates a field where the max length of
the tag is 50 characters'''
class Tag(models.Model):
        tag = models.CharField(max_length= 50)
        def __unicode__(self):
                return self.tag

'''Here I'm creating an Image class. I'm creating a title object where the max
length is 60, the title is allowed to be blank, blank=True, It is also allowed to be blank, null = True.
I create an object where the image field uses fileField, uploads to a file called /images/. I also use a ManyToManyField with Tag and Albums. I add the date theimage was created using the DateTimeField. Uses auto_now_Add-set to true.
Rating is used.Width and height for amending the images at a later point and user- standard procedure. '''

class Image(models.Model):
        title = models.CharField(max_length=60, blank= True, null= True)
        image = models.ImageField(upload_to='images/', blank =True, null=True)
        tags = models.ManyToManyField(Tag, blank=True)
        albums= models.ManyToManyField(Album,blank=True)
        created= models.DateTimeField(auto_now_add = True)
        rating = models.IntegerField(default=50)
        width = models.IntegerField(blank=True, null = True)
        height = models.IntegerField(blank=True, null = True)
        user = models.ForeignKey(User, null= True, blank= True)

        def __unicode__(self):
                return self.image.name

        '''This is the block from before the generating thumbnails section'''
        def save(self, *args, **kwargs):
        	#This saves the image dimensions
        	super(Image, self).save(*args, **kwargs)
            #this saves the image path
        	im = PImage.open(os.path.join(MEDIA_ROOT, self.image.name))
        	self.width, self.height = im.size
        	super(Image, self).save(*args, **kwargs)
        '''
        #Here we're creating thumbnail 2 where thumbnails are uploaded here
        thumbnail2 = models.ImageField(upload_to='images/', blank=True, null = True)

        def save(self, *args, **kwargs):
            #Save image dimensions.
            super(Image, self).save(*args, **kwargs) 
            im = PImage.open(pjoin(MEDIA_ROOT, self.image.name))
            self.width, self.height = im.size

        #large thumbnail
            fn, ext = os.path.splitext(self.image.name)
            im.thumbnail((128,128), PImage.ANTIALIAS)
            thumb_fn = fn + "-thumb2" + ext
        #we're creating a temporary file using tempfile
            tf2 = NamedTemporaryFile()
            im.save(tf2.name, "JPEG")
        #setting save= False as it creates an infinite recursive loop
            self.thumbnail2.save(thumb_fn, File(open(tf2.name)), save = False)
            tf2.close()

        #small thumbnail
            im.thumbnail((40,40), PImage.ANTIALIAS)
            thumb_fn = fn + "-thumb" + ext
            tf = NamedTemporaryFile()
            im.save(tf.name, "JPEG")
            self.thumbnail.save(thumb_fn, File(open(tf.name)), save = False)
            tf.close()

            super(Image, self).save(*args, ** kwargs)'''

        def size(self):
        	#Image size
        	return '%s x %s' % (self.width, self.height)

        def __unicode__(self):
        	return self.image.name

        def tags_(self):
        	# Iterate through all the values in the tag list. Then turn that into a string
        	# and separate with a comma.that returns tuples with primary keys and values we are only interested in values in this case.
        	lst = [x[1] for x in self.tags.values_list()]
        	return str(join(lst, ', '))

        def albums_(self):
        	#Iterate through all the values in the album list. Then turn that into
        	#a separate with a comma. that returns tuples with primary keys and values we are only interested in values in this case.
        	lst = [x[1] for x in self.albums.values_list()]
        	return str(join(lst, ', '))

        def thumbnail(self):
        	#create a link for the image to make it bigger
        	return """<a href='/media/%s'><img border='0' alt '' src='/media/%s' height='40'/></a>"""%((self.image.name, self.image.name))

        thumbnail.allow_tags = True


'''I'm creating album admin field where admin can search by title using the search field. The list display will display lists by titles'''

class AlbumAdmin(admin.ModelAdmin):
        search_fields = ['title']
        list_display = ['title']

'''Tag Admin will display fields by tags'''

class TagAdmin(admin.ModelAdmin):
        list_display =['tag']

'''Image Admin will allow you to search by title, display, title, user, rating and date created in a list format. It also allows you to filter the images by tags and albums'''

class ImageAdmin(admin.ModelAdmin):
        search_fields = ['title']
        list_display = ['__unicode__', 'title', 'user', 'rating', 'size', 'tags_', 'albums_', 'thumbnail', 'created']
        list_filter = ['tags', 'albums','user']

        def save_model(self, request, obj, form, change):
        	obj.user = request.user
        	obj.save()




admin.site.register(Album, AlbumAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Image, ImageAdmin)






