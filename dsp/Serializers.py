from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
import io

from dsp.models import Plc, Room


# class WomenModel:
#     def __init__(self, title, content):
#         self.title = title
#         self.content = content
#
#
# class WomenSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=255)
#     content = serializers.CharField()
#
#
# def encode():
#     women = WomenModel('Lubov', 'Morkov')
#     women_serial = WomenSerializer(women)
#     json = JSONRenderer().render(women_serial.data)
#     print(json)
#
#
# def decode():
#     stream = io.BytesIO(b'{"title":"zhopa", "content":"huy"}')
#     data = JSONParser().parse(stream)
#     serial = WomenSerializer(data=data)
#     serial.is_valid()
#     print(serial.validated_data)


class RoomSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    slag = serializers.SlugField(max_length=255)

    def create(self, validated_data):
        return Room.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.slag = validated_data.get('slag', instance.slag)
        instance.save()
        return instance



class PlcSerializer(ModelSerializer):
    class Meta:
        model = Plc
        fields = ('name', 'description', 'room')

