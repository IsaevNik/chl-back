# coding=utf-8
import json
from rest_framework import serializers

from api.models.point_filled import PointFilled


class PointFilledSerializer(serializers.ModelSerializer):

    type = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    class Meta:
        model = PointFilled
        fields = ('id', 'type', 'content')


    def get_type(self,obj):
        blank = obj.blank
        return blank.get_type_display()


    def get_content(self, obj):
        data = {}
        if obj.blank.type == 2:
            data['blank'] = json.loads(obj.blank.content)
            data['filled'] = json.loads(obj.content)
            return data
        else:
            data['blank'] = obj.blank.content
            data['filled'] = obj.content
        return data


class PointFilledCreateSerializer(serializers.Serializer):
    content = serializers.JSONField()

    def create(self, validated_data, task_filled, blank):
        point_filled = PointFilled(
            blank=blank,
            task_filled=task_filled,
            content=validated_data.get('content'))
        point_filled.save()
