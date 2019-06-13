from django.conf.urls import url

from myapp.views import query, query_uav, query_point, create_line, load_line, echo_once, index, uav_index, uav_move, \
    send_data, create_map

urlpatterns = [
    url(r'^query/$', query, name='query'),
    url(r'^query_uav/(?P<pk>\d+)/$', query_uav, name='query_uav'),
    url(r'^query_point/(?P<pk>\d+)/$', query_point, name='query_point'),
    url(r'^create_line/(?P<pk>\d+)/$', create_line, name='create_line'),
    url(r'^load_line/(?P<pk>\d+)/$', load_line, name='load_line'),
    url(r'^echo_once/$', echo_once),
    url(r'^send_data/(?P<pk>\d+)/$', send_data),
    url(r'^index/$', index),
    url(r'^uav_index/$', uav_index, name='uav_index'),
    url(r'^uav_move/(?P<pk>\d+)/$', uav_move, name='uav_move'),
    url(r'^create_map/$', create_map, name='create_map'),

]
