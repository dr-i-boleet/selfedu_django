from django.db.models import QuerySet
from django.http import HttpResponse, HttpResponseNotFound, Http404

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView

from dsp.forms import *
from dsp.models import *

menu = [{'title': 'О Сайте', 'url_name': 'about'},
        {'title': 'Добавить PLC', 'url_name': 'add_plc'},
        {'title': 'Обратная связь', 'url_name': 'feedback'},
        {'title': 'Войти', 'url_name': 'login'}]


class IndexView(ListView):
    model = Plc
    template_name = 'dsp/index.html'
    context_object_name = 'plc'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Главная страница'
        context['room_sel'] = 0
        return context

    def get_queryset(self):
        return Plc.objects.filter(is_published=True)


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


class AddPlc(CreateView):
    form_class = AddPlcForm
    template_name = 'dsp/add_plc.html'
    #success_url = reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Добавление ПЛК'
        return context


def add_plc(request):
    if request.method == 'POST':
        form = AddPlcForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main')
    else:
        form = AddPlcForm()
    return render(request, 'dsp/add_plc.html', {'form': form, 'menu': menu, 'title': 'Добавить PLC'})


def feedback(request):
    return render(request, 'dsp/feedback.html', {'menu': menu, 'title': 'Обратная связь'})


def login(request):
    return render(request, 'dsp/login.html', {'menu': menu, 'title': 'Войти'})


class PlcView(DetailView):
    model = Plc
    slug_field = 'slag'
    slug_url_kwarg = 'plc_slug'
    context_object_name = 'plc'
    template_name = 'dsp/plc.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = context['plc'].name
        return context


def plc(request, plc_slug):
    plc = Plc.objects.get(slag=plc_slug)
    return render(request, 'dsp/plc.html', {'menu': menu, 'title': 'PLC', 'plc': plc})


class RoomView(ListView):
    model = Plc
    template_name = 'dsp/index.html'
    context_object_name = 'plc'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = context['plc'][0].room.name
        context['room_sel'] = context['plc'][0].room.id
        return context

    def get_queryset(self):
        return Plc.objects.filter(is_published=True, room__slag=self.kwargs['room_slug'])


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
