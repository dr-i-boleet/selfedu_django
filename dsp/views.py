from django.db.models import QuerySet
from django.http import HttpResponse, HttpResponseNotFound, Http404

from django.shortcuts import render, redirect

from dsp.forms import *
from dsp.models import *

menu = [{'title': 'О Сайте', 'url_name': 'about'},
        {'title': 'Добавить PLC', 'url_name': 'add_plc'},
        {'title': 'Обратная связь', 'url_name': 'feedback'},
        {'title': 'Войти', 'url_name': 'login'}]


def index(request):
    context = {
        'menu': menu,
        'plc': Plc.objects.all(),
        'room': Room.objects.order_by('name'),
        'title': 'Главная страница',
        'room_sel': 0
    }
    return render(request, 'dsp/index.html', context=context)


def about(request):
    return render(request, 'dsp/about.html', {'menu': menu, 'title': 'О сайте'})


def add_plc(request):
    if request.method == 'POST':
        form = AddPlcForm(request.POST)
        if form.is_valid():
            try:
                Plc.objects.create(**form.cleaned_data)
                return redirect('main')
            except:
                form.add_error(None, 'Ошибка добавления данных!')

    else:
        form = AddPlcForm()
    return render(request, 'dsp/add_plc.html', {'form': form, 'menu': menu, 'title': 'Добавить PLC'})


def feedback(request):
    return render(request, 'dsp/feedback.html', {'menu': menu, 'title': 'Обратная связь'})


def login(request):
    return render(request, 'dsp/login.html', {'menu': menu, 'title': 'Войти'})


def plc(request, plc_slug):
    plc = Plc.objects.get(slag=plc_slug)
    return render(request, 'dsp/plc.html', {'menu': menu, 'title': 'PLC', 'plc': plc})


def room(request, room_slug):
    rooms = Room.objects.order_by('name')

    try:
        room = Room.objects.get(slag=room_slug)
    except Room.DoesNotExist:
        raise Http404()

    context = {
        'menu': menu,
        'plc': Plc.objects.filter(room=room),
        'room': rooms,
        'title': room.name,
        'room_sel': room.id
    }
    return render(request, 'dsp/index.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('Залупа! Страница не существует!')
