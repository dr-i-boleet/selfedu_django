from django.contrib import admin
from dsp.models import *
# Register your models here.


class PlcAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slag':('name',)}


class RoomAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slag': ('name',)}


admin.site.register(Plc, PlcAdmin)
admin.site.register(Room, RoomAdmin)
