from django.conf.urls import *
from django.contrib import admin
admin.autodiscover()
from register.views import reg
from user_reg.views import FresherRegistration, LoginRequest, LogoutRequest, Home, Theo
from images.views import main, album, image
from django.conf import settings
from theoworld.views import blog, aboutme, projects
from drawingroom.views import blog

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

if settings.DEBUG:
    urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite1.views.home', name='home'),
    # url(r'^mysite1/', include('mysite1.foo.urls')),
        url(r'signup', reg),
        url(r'^register$', FresherRegistration),
        url(r'^login$',LoginRequest),
        url(r'^logout$', LogoutRequest),
        (r'^resetpassword/passwordsent/$', 'django.contrib.auth.views.password_reset_done'),
        (r'^resetpassword/$', 'django.contrib.auth.views.password_reset'),
    #the url below takes the string-toke- and is password reset. it is generated from password reset
        (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    #this method shows a page where the registration is complete
        (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
        (r'^profile$', 'user_reg.views.Profile'),
        (r'home', Home),
        url(r'welcome', reg),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,}),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
        (r"main",'images.views.main'),
        (r"^album/(\d+)/$",'images.views.album'),
        (r"^image/(\d+)/$", 'images.views.image'),
        (r"^pic", "user_reg.views.Profile"),
	    (r"^blog", "theoworld.views.blog"),
	    (r"^aboutme", "theoworld.views.aboutme"),
	    (r"^projects", "theoworld.views.projects"), 
        (r"^drawingroom", "drawingroom.views.blog"),
        (r'^uploadme', 'images.views.ImageInsert'),
        (r'^theo', 'user_reg.views.Theo'),

    # Uncomment the admin/doc line below to enable admin documentation:
        url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	# Uncomment the next line to enable the admin:
        url(r'^admin/', include(admin.site.urls)),

)
