from celery import task

from apiKey import api_key
import ubiClient as ub
import models
import datetime
import pandas

@task()
def add(x, y):
  print "hola mundo!!!"
  return x + y


def get_unique_sensors():
  pass


@task()
def get_all_rest_data():
  print "comenzo el proceso"
  models.Valores.objects.all().delete()
  client = ub.ConnectionUbidots()
  client.authKey(api_key)

  sites= client.getSites()['sites']

  print "num sitios: %s"%len(sites)
  for site in sites:
    vari = client.getVariables(site['domain'])['variables']

  for vr in vari:
    num_pages = client.getValues(vr['id'])['meta']['num_pages']
    print "variable: %s, num paginas:%s"%(vr['name'],num_pages) 

    data =[]
    for i in range(1,num_pages+1):
      vals = client.getValues2(vr["id"],page=i)['values']
      data.extend([
       models.Valores(**{
        "sensor_id":int(vr["id"]),
        "sensor_name":vr["name"],
        "ubiid":int(vl["id"]),
        "timestamp":int(vl["timestamp"]),
        "valor":float(vl["value"])
       })
      for vl in vals]
      )
    print "variable: %s, num valores:%s"%(vr['name'],len(data))
    models.Valores.objects.bulk_create(data)

  return("ok")


