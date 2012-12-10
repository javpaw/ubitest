# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

def actualizar_todos(request):
	return render_to_response('sensors/actualizar_todos.html',{},RequestContext(request))

def actualizar(request):
	from task import get_all_rest_data
	get_all_rest_data.delay()
	return render_to_response('sensors/actualizar.html',{},RequestContext(request))