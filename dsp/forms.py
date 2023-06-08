from django import forms
from django.core.exceptions import ValidationError

from dsp.models import *


#class AddPlcForm(forms.Form):
#    name = forms.CharField(max_length=255, label='Название ПЛК')
#    slag = forms.SlugField(max_length=255, label='Url')
#    description = forms.CharField(widget=forms.Textarea(attrs={'col': 60, 'row': 5}), label='Описание')
#    is_published = forms.BooleanField(initial=True)
#    room = forms.ModelChoiceField(queryset=Room.objects.all(), label='Электропомещение', empty_label='Не задано')

class AddPlcForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room'].empty_label = 'Не задано'

    class Meta:
        model = Plc
        fields = ['name', 'slag', 'description', 'photo', 'is_published', 'room']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 16:
            raise ValidationError('Поле не должно быть длиннее 16 символов')
