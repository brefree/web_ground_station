from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=256)
    password = models.CharField(max_length=256)


# 用户
class UavUser(models.Model):
    # 用户名
    nickname = models.CharField(verbose_name='昵称', max_length=256)
    # 密码
    hash_password = models.CharField(verbose_name='密码', max_length=256)
    # 电话
    phone = models.CharField(verbose_name='电话', max_length=11)
    # 权限
    permission = models.ForeignKey('Permission', verbose_name='权限', related_name='uav_user')
    # 删除
    is_delete = models.BooleanField(verbose_name='删除', default=False)
    # 创建时间
    data_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


# 指令表
class Command(models.Model):
    # 用户id
    # 飞机id
    # 架次id
    # 创建时间
    # 指令id
    pass


# 权限
class Permission(models.Model):
    name = models.CharField(max_length=256)


# 规划航点表
class PlanPoint(models.Model):
    # 航点编号
    point_id = models.CharField(max_length=256, blank=True, null=True)
    # 经度
    longitude = models.CharField(max_length=256, blank=True, null=True)
    # 纬度
    latitude = models.CharField(max_length=256, blank=True, null=True)
    # 高度
    altitude = models.CharField(max_length=256, blank=True, null=True)
    # 航线编号
    line = models.ForeignKey('PlanLine')
    # 创建时间
    data_time = models.DateTimeField(auto_now_add=True)


# 规划航线表
class PlanLine(models.Model):
    # 航线编号
    line_id = models.CharField(max_length=256)
    # 起飞点名称
    start_point = models.CharField(max_length=256, null=True, blank=True)
    # 起飞点经度
    start_longitude = models.CharField(max_length=256)
    # 起飞点纬度
    start_latitude = models.CharField(max_length=256)
    # 降落点名称
    end_point = models.CharField(max_length=256, null=True, blank=True)
    # 降落点经度
    end_longitude = models.CharField(max_length=256, blank=True, null=True)
    # 降落度纬度
    end_latitude = models.CharField(max_length=256, blank=True, null=True)
    # 创建时间
    data_time = models.DateTimeField(auto_now_add=True)


class RealPoint(models.Model):
    # 实时航点编号
    real_id = models.CharField(max_length=256, blank=True, null=True)
    # 经度
    real_longitude = models.CharField(max_length=256, blank=True, null=True)
    # 纬度
    real_latitude = models.CharField(max_length=256, blank=True, null=True)
    # 高度
    real_altitude = models.CharField(max_length=256, blank=True, null=True)
    # 水平速度
    real_hs = models.CharField(max_length=256, blank=True, null=True)
    # 竖直速度
    real_vs = models.CharField(max_length=256, blank=True, null=True)
    # gps数量
    real_count = models.CharField(max_length=256, blank=True, null=True)
    # 剩余电量
    real_battery = models.CharField(max_length=256, blank=True, null=True)
    # 横滚角
    real_roll = models.CharField(max_length=256, blank=True, null=True)
    # 俯仰角
    real_pitch = models.CharField(max_length=256, blank=True, null=True)
    # 架次编号
    sortie = models.ForeignKey('UavData', null=True, blank=True)
    # 飞机编号
    uav = models.ForeignKey('Uav')
    # 创建时间
    data_time = models.DateTimeField(auto_now_add=True)


# 飞行架次表
class UavData(models.Model):
    sortie_choices = (
        (1, '选中'),
        (2, '已完成'),
    )
    # 架次编号
    sortie_py = models.CharField(max_length=256, blank=True, null=True)
    # 航线编号
    line = models.ForeignKey('PlanLine')
    # 飞机编号
    uav = models.ForeignKey('Uav')
    # 创建时间
    data_time = models.DateTimeField(auto_now_add=True)
    # 状态
    status = models.PositiveSmallIntegerField('状态', choices=sortie_choices, default=1)


# 飞机管理表
class Uav(models.Model):
    uav_status = (
        (1, '在线'),
        (2, '离线'),
        (3, '维修'),
    )
    # 飞机编号
    uav_id = models.CharField(max_length=256)
    # 飞机名称
    uav_name = models.CharField(max_length=256)
    # 飞机型号
    uav_model = models.ForeignKey('UavType')
    # 飞机管理员
    uav_admin = models.ForeignKey('UavUser')
    # 创建时间
    data_time = models.DateTimeField(auto_now_add=True)
    ip = models.CharField('地址', max_length=16, default='0.0.0.0')
    status = models.PositiveSmallIntegerField('状态', choices=uav_status, default=2)


# 飞机类型表
class UavType(models.Model):
    name = models.CharField('型号名称', max_length=256, blank=True, null=True)
    type = models.CharField('飞机类型', max_length=256, blank=True, null=True)
    weight = models.CharField('飞机自重', max_length=256, blank=True, null=True)
    normal_fly_weight = models.CharField('标准起飞重量', max_length=256, blank=True, null=True)
    max_fly_weight = models.CharField('最大起飞重量', max_length=256, blank=True, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('创建时间', auto_now=True)
    status = models.PositiveSmallIntegerField('状态',)
