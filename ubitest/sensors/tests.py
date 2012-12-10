"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import sys

from django.test import TestCase
from apiKey import api_key
import ubiClient as ub
import models
import datetime
from django.core import serializers
import json

class SimpleTest(TestCase):
  def test_basic_addition(self):
      """
      Tests that 1 + 1 always equals 2.
      """
      self.assertEqual(1 + 1, 2)


class RestTest(TestCase):

  def setUp(self):
    self.client = ub.ConnectionUbidots()
    self.client.authKey(api_key)


  def test_rest_get_site_exp(self):
    """
    Testing del servicio rest de ubidots - experimento
    """

    sites= self.client.getSites()['sites']
    print sites
    sys.stdout.flush()

  def test_rest_get_vars_exp(self):
    """
    Testing del servicio rest de ubidots obtener variables
    """
    client = self.client

    sites= client.getSites()['sites']

    for site in sites:
      vari = client.getVariables(site['domain'])['variables']
      ids = [vr['id']  for vr in vari]
      print vari

  def test_fill_db(self):
    models.Valores.objects.bulk_create([
      models.Valores(**{"sensor_id":1,"sensor_name":"sen1","ubiid":1,
        "fecha":datetime.datetime.now(),"valor":1.23})
    ])

    print models.Valores.objects.get(pk=1)

  def test_type_of_vars(self):
    """
    Que tipo tienen los datos enviados por el servicio?
    Segun este test son strings (unicode)
    """
    client = self.client

    sites= client.getSites()['sites']
    #Obteniendo ids de  variables
    for site in sites:
      vari = client.getVariables(site['domain'])['variables']
      ids = [vr['id']  for vr in vari] #I'll use vari name and vari id

    vals = client.getValues(ids[0])['values'][0]
    for k in vals.keys():
      print k, type(k)



  def test_rest_store_in_db(self):
    client = self.client

    sites= client.getSites()['sites']
    #Obteniendo ids de  variables
    for site in sites:
      vari = client.getVariables(site['domain'])['variables']
      ids = [vr['id']  for vr in vari] #I'll use vari name and vari id

    for vr in vari:
      num_pages = client.getValues(vr['id'])['meta']['num_pages']

      data =[]
      #patch para hacer el test mas rapido:
      #num_pages = 2
      for i in range(1,num_pages):
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

      models.Valores.objects.bulk_create(data)


    #get distinct sensors
    r = models.Valores.objects.all().values_list('sensor_id',flat=True)
    r = list(set(r))
    print r

    #serialize to save the fixture
    data = serializers.serialize("json", models.Valores.objects.all())
    f = open("/tmp/fixture","w")
    f.write(json.dumps(data))
    f.close()

    #get max timestamp for each sensor

      
    print models.Valores.objects.get(pk=1).sensor_name #gen1
    print models.Valores.objects.count()

  def test_celery_easy(self):
    """Test that the ``add`` task runs with no errors,
    and returns the correct result."""
    from tasks import add
    result = add.delay(8, 8)

    self.assertEquals(result.get(), 16)
    self.assertTrue(result.successful())

  def test_read_json(self):
    f = open("/tmp/fixture",'r')
    f2 = open("/tmp/fixture_2",'w')
    f2.write( json.dumps(json.loads(json.loads(f.read()))) )
    f.close()
    f2.close()
