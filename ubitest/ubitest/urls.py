from django.conf.urls import patterns, include, url
from django.contrib import admin

from sensors.views import actualizar_todos,actualizar,por_horas,por_dias,total,postear_horas,postear_dias,resultado_total

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
	url(r'^$', 'django.views.generic.simple.direct_to_template',{'template':'sensors/sensors_index.html'}),
	url(r'^actualizar_todos', actualizar_todos),
	url(r'^actualizar', actualizar),
	url(r'^por_horas',por_horas),
	url(r'^por_dias',por_dias),
	url(r'^postear_horas',postear_horas),
	url(r'^postear_dias',postear_dias),
	url(r'^resultado_total',resultado_total),
	url(r'^total',total),
)
