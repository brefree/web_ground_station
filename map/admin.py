from django.contrib import admin
from .models import *


# Register your models here.
class UavUserAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'hash_password', 'phone', 'permission', 'is_delete', 'data_time']


class PermissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class PlanPointAdmin(admin.ModelAdmin):
    list_display = ['point_id', 'longitude', 'latitude', 'line_id', 'data_time']


class PlanLineAdmin(admin.ModelAdmin):
    list_display = ['line_id', 'start_point', 'start_longitude', 'start_latitude', 'end_point', 'end_longitude',
                    'end_latitude', 'data_time']


admin.site.register(UavUser, UavUserAdmin)
