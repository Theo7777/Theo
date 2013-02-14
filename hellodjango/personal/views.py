
# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from hellodjango.settings import MEDIA_URL, MEDIA_ROOT
from django.http import HttpResponse

def Homepage(request):
	return render_to_response('parallax.html', context_instance = RequestContext(request))
