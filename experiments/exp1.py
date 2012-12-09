import ubiClient as ub
from apiKey import api_key
import json

client = ub.ConnectionUbidots()
client.authKey(api_key)

#Obteniendo los sitios
sites= client.getSites()['sites']


#Obteniendo ids de  variables
for site in sites:
  vari = client.getVariables(site['domain'])['variables']
  ids = [vr['id']  for vr in vari]
  print ids


for sid in ids[:2]:
  print "in %s"%sid
  num_pages = client.getValues(sid)['meta']['num_pages']
  data =[]
  for i in range(1,num_pages+1):
    data.extend(client.getValues2(sid,page=i)['values'])
  f = open(str(sid)+".json",'w')

  f.write(json.dumps(data))
  f.close()
  #obtener todos los datos de un sensor:
