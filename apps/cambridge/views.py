from django.contrib.auth.decorators import login_required, permission_required

from django.template.loader import render_to_string
from django.template import RequestContext

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

import StringIO
import ho.pisa as pisa

from django_xhtml2pdf.utils import render_to_pdf_response

from models import *

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def ver(request, pk):
	registration = get_object_or_404(Registration, id=pk)
	payload = {'registration': registration}
	file_data = render_to_string('cambridge/imprimir.html', payload, RequestContext(request))
	myfile = StringIO.StringIO()
	return HttpResponse( file_data )

def fetch_resources(uri, rel):
    #path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    path = settings.MEDIA_ROOT + uri
    return path	

def imprimir(registration,request):
	payload = {'registration': registration}
	file_data = render_to_string('cambridge/imprimir.html', payload, RequestContext(request))
	myfile = StringIO.StringIO()
	pisa.CreatePDF(file_data, myfile, link_callback=fetch_resources)
	myfile.seek(0)
	response =  HttpResponse(myfile, mimetype='application/pdf')
	response['Content-Disposition'] = 'attachment; filename=cambridge-%s.pdf'%registration.id
	response2 = render_to_pdf_response('cambridge/imprimir.html', payload, 'cambridge-%s.pdf'%registration.id)
	return response2

@login_required
def imprimir_cambridge(request, pk):
	logger.debug("Vamos a imprimir una matricula normal")
	registration = Registration.objects.get(id=pk)
	return imprimir(registration,request)


@login_required
def imprimir_cambridge_cb(request, pk):
	logger.debug("Vamos a imprimir una matricula normal Computer based")
	registration = ComputerBasedRegistration.objects.get(id=pk)
	return imprimir(registration)
