from django import forms
from dsp.models import *


class AddPlcForm(forms.Form):
    name = forms.CharField(max_length=255, label='Название ПЛК')
    slag = forms.SlugField(max_length=255, label='Url')
    description = forms.CharField(widget=forms.Textarea(attrs={'col': 60, 'row': 5}), label='Описание')
    is_published = forms.BooleanField(initial=True)
    room = forms.ModelChoiceField(queryset=Room.objects.all(), label='Электропомещение', empty_label='Не задано')

