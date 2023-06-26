from django.contrib import admin
from dsp.models import *
# Register your models here.


class PlcAdmin(admin.ModelAdmin):
    #Поля, отображаемые в списке записей Plc
    list_display = ('id', 'name', 'dt_updated', 'get_photo_image', 'is_published', 'room')
    list_editable = ('is_published',)
    list_display_links = ('id', 'name')

    #Slug формируется на основе поля name
    prepopulated_fields = {'slag':('name',)}

    def get_photo_image(self, obj):
        # obj - объект класса Plc
        if obj.photo:
            return mark_safe(f'<a href="{obj.photo.url}"><img src="{obj.photo.url}" width=50></a>')

    get_photo_image.short_description = 'Фото'

    readonly_fields = ('get_photo_image', 'dt_created', 'dt_updated')
    fields = ('name', 'slag', 'description', 'room', 'photo', 'get_photo_image', 'is_published', 'dt_created', 'dt_updated')


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    ordering = ('id',)
    prepopulated_fields = {'slag': ('name',)}


admin.site.register(Plc, PlcAdmin)
admin.site.register(Room, RoomAdmin)
