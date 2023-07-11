from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.models import QuerySet
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseNotFound, Http404

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, \
    RetrieveDestroyAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from dsp.Serializers import PlcSerializer, RoomSerializer, RoomModelSerializer
from dsp.forms import *
from dsp.permissions import IsOwnerOrReadOnly
from dsp.utils import *

menu = [{'title': 'О Сайте', 'url_name': 'about'},
        {'title': 'Обратная связь', 'url_name': 'feedback'}]


class IndexView(DataMixin, ListView):
    model = Plc
    template_name = 'dsp/index.html'
    context_object_name = 'plc'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(user_context.items()))

    def get_queryset(self):
        return Plc.objects.filter(is_published=True).select_related('room')


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


class AddPlc(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPlcForm
    template_name = 'dsp/add_plc.html'
    #success_url = reverse_lazy('main')
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Добавление PLC', room_sel=-1)
        return dict(list(context.items()) + list(user_context.items()))


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


class PlcView(DataMixin, DetailView):
    model = Plc
    slug_field = 'slag'
    slug_url_kwarg = 'plc_slug'
    context_object_name = 'plc'
    template_name = 'dsp/plc.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title=context['plc'].name)
        return dict(list(context.items()) + list(user_context.items()))


def plc(request, plc_slug):
    plc = Plc.objects.get(slag=plc_slug)
    return render(request, 'dsp/plc.html', {'menu': menu, 'title': 'PLC', 'plc': plc})


class RoomView(DataMixin, ListView):
    model = Plc
    template_name = 'dsp/index.html'
    context_object_name = 'plc'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        r = Room.objects.get(slag=self.kwargs['room_slug'])
        user_context = self.get_user_context(title=r.name, room_sel=r.id)
        return dict(list(context.items()) + list(user_context.items()))

    def get_queryset(self):
        return Plc.objects.filter(is_published=True, room__slag=self.kwargs['room_slug']).select_related('room')


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


class RegisterView(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'dsp/register.html'
    context_object_name = 'user'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Регистрация', room_sel=-1)
        return dict(list(context.items()) + list(user_context.items()))


class LoginUserView(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'dsp/login.html'
    print("!!!")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'load_count' not in self.request.session:
            load_count = 0
        else:
            load_count = self.request.session['load_count']

        user_context = self.get_user_context(title='Авторизация', load_count=load_count)
        return dict(list(context.items()) + list(user_context.items()))

    def get_form_class(self):
        if 'load_count' not in self.request.session:
            load_count = 0
        else:
            load_count = self.request.session['load_count']

        print("get form class")
        print(load_count)
        if load_count > 3:
            return LoginUserFormCaptcha
        return LoginUserForm

    def get_success_url(self):
        return reverse_lazy('main')

    def form_valid(self, form):
        self.request.session['load_count'] = 0
        return super().form_valid(form)

    def form_invalid(self, form):
        if 'load_count' in self.request.session:
            print(self.request.session['load_count'])
            if self.request.session['load_count'] < 4:
                self.request.session['load_count'] = self.request.session['load_count'] + 1
        else:
            self.request.session['load_count'] = 1

        return super().form_invalid(form)


def logout_user(request):
    logout(request)
    return redirect('main')


class PlcApiView(ListAPIView):
    queryset = Plc.objects.all()
    serializer_class = PlcSerializer


class PlcGenApiView(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        return Response({'rooms:': RoomSerializer(rooms, many=True).data})

    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'room': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)

        if not pk:
            return Response({'Error': 'Methon PUT not allowed'})

        try:
            room = Room.objects.get(pk=pk)
        except:
            return Response({'Error': 'Object not found'})

        serializer = RoomSerializer(instance=room, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'room': serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)

        if not pk:
            return Response({'Error', 'Method DELETE not allowed'})

        try:
            room = Room.objects.get(pk=pk)
        except:
            return Response({'Error': 'Object not found'})

        serializer = RoomSerializer(room)
        room.delete()
        return Response({'room deleted': serializer.data})


class RoomListCreateApiView(ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomModelSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class RoomUpdateApiView(RetrieveUpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomModelSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class RoomDestroyApiView(RetrieveDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomModelSerializer
    permission_classes = (IsAdminUser,)


class RoomViewSet(ModelViewSet):
    # queryset = Room.objects.all()
    serializer_class = RoomModelSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if not pk:
            return Room.objects.all()

        return Room.objects.filter(pk=pk)

    @action(methods=['get',], detail=True)
    def plc(self, request, pk=None):
        return Response({'plc': Plc.objects.get(pk=pk).name})


