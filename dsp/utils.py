from django.db.models import Count

from dsp.models import *

menu = [{'title': 'О Сайте', 'url_name': 'about'},
        {'title': 'Добавить PLC', 'url_name': 'add_plc'},
        {'title': 'Обратная связь', 'url_name': 'feedback'},
        {'title': 'Войти', 'url_name': 'login'}]


class DataMixin:
    paginate_by = 1

    def get_user_context(self, **kwargs):
        context = kwargs
        if self.request.user.is_authenticated:
            context['menu'] = menu
        else:
            guest_menu = menu.copy()
            guest_menu.pop(1)
            context['menu'] = guest_menu

        context['room'] = Room.objects.order_by('name').annotate(count=Count('plc__id'))
        if 'room_sel' not in context:
            context['room_sel'] = 0

        return context

