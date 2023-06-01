from django.http import HttpResponse, HttpResponseNotFound

from django.shortcuts import render, redirect
from dsp.models import *


menu = [{'title': 'О Сайте', 'url_name': 'about'},
        {'title': 'Добавить PLC', 'url_name': 'add_plc'},
        {'title': 'Обратная связь', 'url_name': 'feedback'},
        {'title': 'Войти', 'url_name': 'login'}]


def index(request):
    context = {
        'menu': menu,
        'plc': Plc.objects.all(),
        'title': 'Главная страница'
    }
    return render(request, 'dsp/index.html', context=context)


def about(request):
    return render(request, 'dsp/about.html', {'menu': menu, 'title': 'О сайте'})


def add_plc(request):
    return render(request, 'dsp/add_plc.html', {'menu': menu, 'title': 'Добавить PLC'})


def feedback(request):
    return render(request, 'dsp/feedback.html', {'menu': menu, 'title': 'Обратная связь'})


def login(request):
    return render(request, 'dsp/login.html', {'menu': menu, 'title': 'Войти'})


def plc(request, plc_id):
    plc = Plc.objects.get(id=plc_id)
    return render(request, 'dsp/plc.html', {'menu': menu, 'title': 'PLC', 'plc': plc})


def rooms(request, roomid):
    if request.GET:
        return HttpResponse(f"<h1>Электропомещения</h1><p>{request.GET['room']}</p>")

    if roomid > 100:
        return redirect('main')
    return HttpResponse(f'<h1>Электропомещения</h1><p>{roomid}</p>')


def pageNotFound(request, exception):
    return HttpResponseNotFound('Залупа! Страница не существует!')

