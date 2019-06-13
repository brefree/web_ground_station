import json
import random
import time
import uuid

from django.core import serializers
from django.forms import model_to_dict
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from dwebsocket.decorators import accept_websocket, require_websocket
from django.http import HttpResponse
from dwebsocket.websocket import WebSocket

from myapp.models import *

uav_id = []
uav_longitude = []
uav_latitude = []
my_message = None
temp = []


# 发送数据
@require_websocket
def send_data(request, pk):
    if not request.is_websocket():  # 判断是不是websocket连接
        # 如果是普通的http方法
        return render(request, 'map_move.html')
    else:
        # while my_message:
        # request.websocket.send(my_message)
        #   time.sleep(1)
        # for i in range(10):
        #     request.websocket.send(my_message)
        #     time.sleep(0.5)
        while True:
            data = RealPoint.objects.filter(uav_id=pk).last()
            # ret = serializers.serialize("json", data)
            ret = model_to_dict(data)
            request.websocket.send(json.dumps(ret).encode())
            time.sleep(1)


# 双向通信
@require_websocket
def echo_once(request):
    global my_message
    if not request.is_websocket():  # 判断是不是websocket连接
        # 如果是普通的http方法
        try:
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request, 'index.html')
    else:
        for message in request.websocket:
            if not message:
                break
            my_message = message
            my_list = message.decode('utf-8').split(',')
            real_point = RealPoint()
            real_point.real_id = my_list[1]
            real_point.real_longitude = my_list[3]
            real_point.real_latitude = my_list[5]
            real_point.real_altitude = my_list[7]
            real_point.real_hs = my_list[9]
            real_point.real_vs = my_list[11]
            real_point.real_count = my_list[13]
            real_point.real_battery = my_list[15]
            real_point.real_roll = my_list[17]
            real_point.real_pitch = my_list[19]
            print(my_list)
            # print(my_list[21])
            sortie = UavData.objects.get(pk=my_list[21])

            real_point.sortie = sortie
            uav = Uav.objects.get(pk=my_list[23])
            real_point.uav = uav
            real_point.save()
            # 发送消息到客户端
            request.websocket.send(message)
            if my_list[-1] not in uav_id:
                uav_id.append(my_list[-1])
                uav_longitude.append(my_list[3])
                uav_latitude.append(my_list[5])
                # print(type(message))
                # my_dict = eval(message.decode('utf-8'))
                # my_dict = json.load(message.decode('utf-8'))
                # print(my_dict,type(my_dict))
                # uav_id.append(my_dict['pk'])
                # print(my_dict,type(my_dict))
        my_message = None


def index(request):
    return render(request, 'index.html')


# 监控页面,pk为飞机id
def uav_move(request, pk):
    point_list = []
    sortie = UavData.objects.filter(uav_id=pk).filter(status=1).last()
    if sortie:
        line = sortie.line
        point_list = line.planpoint_set.all()
    real_point = RealPoint.objects.filter(uav_id=pk).last()
    return render(request, 'myapp/map_move.html',
                  {'real_point': real_point, 'point_list': point_list, 'pk': pk})


# 飞机首页
# def uav_index(request):
#     uavs = Uav.objects.filter(status=1)
#     uav_id = []
#     uav_longitude = []
#     uav_latitude = []
#     for uav in uavs:
#         uav_id.append(uav.id)
#         real_point = RealPoint.objects.filter(uav_id=uav.id).last()
#         uav_latitude.append(real_point.real_latitude)
#         uav_longitude.append(real_point.real_longitude)
#     return render(request, 'map_bg.html',
#                   {'uav_id': uav_id, 'uav_longitude': uav_longitude, 'uav_latitude': uav_latitude})


# 飞机首页
def uav_index(request):
    uavs = Uav.objects.filter(status=1)
    return render(request, 'myapp/uav_index.html', {'uavs': uavs})


# 查询所有飞机数据1
def query(request):
    sortie = UavData.objects.all()
    return render(request, 'myapp/query.html', {'sortie': sortie})


# 查询飞机
def query_uav(request, pk):
    uav = Uav.objects.get(pk=pk)
    sortie = uav.uavdata_set.all()
    return render(request, 'myapp/query.html', {'sortie': sortie})


# 查询航点
def query_point(request, pk):
    sortie = UavData.objects.get(pk=pk)
    points = sortie.realpoint_set.all()
    return render(request, 'myapp/query_point.html', {'points': points})


# 创建航线,pk为飞机编号
def create_line(request, pk):
    if request.method == 'POST':
        # uav = Uav.objects.get(pk=pk)
        longitude = request.POST.getlist('longitude')
        latitude = request.POST.getlist('latitude')
        altitude = request.POST.getlist('altitude')
        plan_line = PlanLine(line_id=uuid.uuid1(), start_point=uuid.uuid1(), start_longitude=longitude[0],
                             start_latitude=latitude[0], end_point=uuid.uuid1(), end_longitude=longitude[-1],
                             end_latitude=longitude[-1])
        plan_line.save()
        for i in range(len(longitude)):
            plan_point = PlanPoint(point_id=uuid.uuid1(), longitude=longitude[i], latitude=latitude[i],
                                   altitude=altitude[i], line_id=plan_line.id)
            plan_point.save()

        uav_data = UavData(sortie_py=uuid.uuid1(), line_id=plan_line.id, uav_id=pk)
        uav_data.save()
        print('储存成功！')
        return redirect(reverse('load_line', kwargs={'pk': plan_line.id}))
    return render(request, 'myapp/map_index.html')


def create_map(request):
    return render(request, 'myapp/map_index.html')


# 加载航线,pk为航线id
def load_line(request, pk):
    line = PlanLine.objects.get(pk=pk)
    point_list = line.planpoint_set.all()
    longitude_list = []
    latitude_list = []
    altitude_list = []
    for point in point_list:
        longitude_list.append(point.longitude)
        latitude_list.append(point.latitude)
        altitude_list.append(point.altitude)
    print(longitude_list, latitude_list, altitude_list)
    return render(request, 'myapp/map_load.html',
                  {'longitude_list': longitude_list, 'latitude_list': latitude_list, 'altitude_list': altitude_list,
                   'point_list': point_list})

# 通讯方式为socket,客户端连接上服务器后,服务器获取客户端的地址(创建对象,状态为在线)
# socket连接成功后,校验客户端发送的数据是否符合规则,符合则创建状态记录表单(此处后期可改为redis缓存,sql持久化)
# 若断开连接,则将此对象状态设置为离线
# 首页通信方式为http,用户每发起一次请求,查询一次数据库,查询内容为所有状态为在线的设备
# 观看航线页面,为使用websocket拿取最新的一条状态记录数据(redis缓存为拿取redis中最新的数据)
