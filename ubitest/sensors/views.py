# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import pandas as pd

def actualizar_todos(request):
  return render_to_response('sensors/actualizar_todos.html',{},RequestContext(request))

def actualizar(request):
  from tasks import get_all_rest_data
  get_all_rest_data.delay()
  return render_to_response('sensors/actualizar.html',{},RequestContext(request))


def por_horas(request):
  from tasks import calculate_per_hour
  result = calculate_per_hour()
  result = [{'sensor':i[0],'hora':i[1],'valor':i[2] } for i in
      zip(list(result['sensor_name']),list(result['hora']),list(result['valor']) )
  ]
  print result
  return render_to_response("sensors/por_hora.html",{'resultado':result,'postear':"/postear_horas" },RequestContext(request))


def por_dias(request):
  from tasks import calculate_per_days
  result = calculate_per_days()
  result = [{'sensor':i[0],'hora':i[1],'valor':i[2] } for i in
      zip(list(result['sensor_name']),list(result['hora']),list(result['valor']) )
  ]
  print result
  return render_to_response("sensors/por_hora.html",{'resultado':result,'postear':"/postear_dias" },RequestContext(request))

def total(request):
    from tasks import calculate_total
    result = int(calculate_total()/1000)
    return render_to_response("sensors/total.html",{"resultado":result},RequestContext(request))


def postear_horas(request):
  from tasks import post_to_ubidots
  post_to_ubidots.delay()
  return render_to_response("sensors/posteando.html",{},RequestContext(request))


def postear_dias(request):
  from tasks import post_to_ubidots
  post_to_ubidots.delay(time='days')
  return render_to_response("sensors/posteando.html",{},RequestContext(request))


def resultado_total(request):
  from tasks import post_grant_result
  post_grant_result.delay()
  return render_to_response("sensors/posteando.html",{},RequestContext(request))
