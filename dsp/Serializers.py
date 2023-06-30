from rest_framework.serializers import ModelSerializer

from dsp.models import Plc


class PlcSerializer(ModelSerializer):
    class Meta:
        model = Plc
        fields = ('name', 'description', 'room')

