from django.db import models

class Valores(models.Model):
  sensor_id = models.IntegerField()
  sensor_name = models.CharField(max_length=50)
  ubiid = models.IntegerField()
  timestamp = models.IntegerField()
  valor = models.FloatField()