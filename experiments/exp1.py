import ubiClient as ub
from apiKey import api_key
client = ub.ConnectionUbidots()
client.authKey(api_key)

#Obteniendo los sitios
sites= client.getSites()['sites']


#Obteniendo ids de  variables
for site in sites:
  vari = client.getVariables(site['domain'])['variables']
  ids = [vr['id']  for vr in vari]
  print ids

#num_pages = client.getValues
#obtener todos los datos de un sensor:
