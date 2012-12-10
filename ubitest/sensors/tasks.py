from celery import task

from apiKey import api_key
import ubiClient as ub
import models
import datetime
import time
import pandas as pd

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
  print "todos los datos han sido borrados"
  print "numero valores: %i"%models.Valores.objects.all().count()
  client = ub.ConnectionUbidots()
  client.authKey(api_key)

  sites= client.getSites()['sites']

  print "num sitios: %s"%len(sites)
  for site in sites:
    vari = client.getVariables(site['domain'])['variables']

  vari = [i for i in vari if i['name'] in ['gen1','gen2','gen3'] ]
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

def calculate_per_hour():
  """
  Calcula la generacion de energia de cada uno de los tres generadores
  por hora
  """

  #De Base de datos a dataframe
  datos = pd.DataFrame(list(models.Valores.objects.all().values('sensor_id','sensor_name','timestamp','valor')))
  print type(datos)
  #Asegurar tipos en Dataframe
  datos['valor'] = datos['valor'].apply(float)

  #Calcular tiempo
  a =datos['timestamp']/1000
  a =a.apply(datetime.datetime.fromtimestamp)
  datos['time']=a

  #Ordenar por tiempo ascendentemente
  datos = datos.sort('time',ascending=True)

  #Funcion para quedar solo con la hora
  def cut_minute(date):
    return date.replace(minute=0)

  #Nueva columna donde se ignoran los minutos
  datos['hora'] = datos['time'].apply(cut_minute)

  #Agrupar por horas y calculo de Energia por hora
  porhoras = datos.groupby(['sensor_name','sensor_id','hora']).valor.sum()

  #Resetear el indice
  porhoras =porhoras.reset_index()

  #Calcular el timestamp
  porhoras['timestamp'] = porhoras['hora'].apply(lambda x: int(
      time.mktime( pd.Timestamp(x).timetuple())  )*1000
    )

  #En este momento se tiene las columnas
  #sensor_name  sensor_id hora  valor timestamp
  return porhoras


def calculate_per_days():
  """
  Calcula la generacion de energia de cada uno de los tres generadores
  por hora
  """

  #De Base de datos a dataframe
  datos = pd.DataFrame(list(models.Valores.objects.all().values('sensor_id','sensor_name','timestamp','valor')))
  print type(datos)
  #Asegurar tipos en Dataframe
  datos['valor'] = datos['valor'].apply(float)

  #Calcular tiempo
  a =datos['timestamp']/1000
  a =a.apply(datetime.datetime.fromtimestamp)
  datos['time']=a

  #Ordenar por tiempo ascendentemente
  datos = datos.sort('time',ascending=True)

  #Funcion para quedar solo con la hora
  def cut_hour_minute(date):
    return date.replace(hour=0,minute=0)

  #Nueva columna donde se ignoran los minutos
  datos['hora'] = datos['time'].apply(cut_hour_minute)

  #Agrupar por horas y calculo de Energia por hora
  pordias = datos.groupby(['sensor_name','sensor_id','hora']).valor.sum()

  #Resetear el indice
  pordias =pordias.reset_index()

  #Calcular el timestamp
  pordias['timestamp'] = pordias['hora'].apply(lambda x: int(
      time.mktime( pd.Timestamp(x).timetuple())  )*1000
    )
  
  #En este momento se tiene las columnas
  #sensor_name  sensor_id hora  valor timestamp
  return pordias

def calculate_total():
  pd = calculate_per_days()
  return pd.valor.sum()