from django import template
from dsp.models import *

register = template.Library()


@register.inclusion_tag('dsp/show_rooms.html')
def show_room(room_sel=0):
    return {'room': Room.objects.order_by('name'), 'room_sel': room_sel}
