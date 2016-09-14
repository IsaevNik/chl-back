# coding=utf-8
import json
from rest_framework import serializers
from django.db import transaction

from api.models.point_blank import PointBlank


class PointBlankSerializer(serializers.ModelSerializer):

    type = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    class Meta:
        model = PointBlank
        fields = ('id', 'task', 'type', 'order', 'expl_image',
            'content')

    def get_type(self,obj):
        return obj.get_type_display()


    def get_content(self, obj):
        if obj.type == 2:
            data = json.loads(obj.content)
            return data
        else:
            return obj.content

class PoinBlankCreateSerializer(serializers.Serializer):

    order = serializers.IntegerField()
    expl_image = serializers.CharField(default=None)
    content = serializers.JSONField()
    type = serializers.IntegerField()
    id = serializers.IntegerField(default=0)


    def create(self, validated_data, task):
        point_blank = PointBlank(
            order = validated_data['order'],
            expl_image=validated_data['expl_image'],
            content=validated_data['content'],
            type=validated_data['type'],
            task=task)
        point_blank.save()


    def update(self, point_blank, validated_data):
        point_blank.order = validated_data['order']
        point_blank.expl_image = validated_data['expl_image']
        point_blank.content = validated_data['content']
        point_blank.type = validated_data['type']
        point_blank.save()



