# coding=utf-8
from rest_framework import serializers
from django.db import transaction
from django.utils import timezone

from api.models.task_filled import TaskFilled
from api.models.task import Task
from api.models.task_address import TaskAddress
from task import TaskForManySerializer
from point_filled import PointFilledSerializer
from agent import AgentSerializer
from task_address import TaskWithAddressSerializer
 
class TaskForDetailSerializer(TaskForManySerializer):
    blanks = serializers.IntegerField(source='blanks_count')

# MOBILE VERSION
class TaskAddressWebSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskAddress
        fields = ('id', 'address', 'longitude', 'latitude', 'distance')


class TaskShortWebSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'price')


class TaskFilledListMobileSerializer(serializers.ModelSerializer):
    task = TaskShortWebSerializer(source='task_address.task')
    check_dt = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    status = serializers.SerializerMethodField()
    task_address = TaskAddressWebSerializer()

    class Meta:
        model = TaskFilled
        fields = ('id', 'task_address', 'task', 'status', 'comment', 'check_dt')

    def get_status(self,obj):
        return obj.get_status_display()
#####

# WEB VERSION
class TaskShortWebSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'client_name')


class TaskFilledListWebSerializer(serializers.ModelSerializer):

    task_address = serializers.CharField(source='task_address.address')
    task = TaskShortWebSerializer(source='task_address.task')
    status = serializers.SerializerMethodField()
    executer = AgentSerializer()
    
    class Meta:
        model = TaskFilled
        fields = ('id', 'task_address', 'task', 'executer', 'status')

    def get_status(self,obj):
        return obj.get_status_display()


class TaskFilledDetailWebSerializer(serializers.ModelSerializer):

    take_dt = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    end_dt = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    check_dt = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    task = TaskForDetailSerializer(source='task_address.task')
    filled_blanks = PointFilledSerializer(many=True)
    executer = AgentSerializer()

    class Meta:
        model = TaskFilled
        depth = 1
        fields = ('id', 'task_address', 'task', 'executer', 'take_dt', 'end_dt', \
                  'check_dt', 'longitude', 'latitude', 'filled_blanks')
#####

class TaskFilledUpdateSerializer(serializers.Serializer):
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
    task = serializers.CharField()

    def update(self, task_filled, validated_data):
        task_filled.longitude = validated_data['longitude']
        task_filled.latitude = validated_data['latitude']
        task_filled.end_dt = timezone.now()
        task_filled.status = 1
        task_filled.save()




class CheckingTaskSerializer(serializers.Serializer):
    comment = serializers.CharField(default='')
    points = serializers.IntegerField(default=0)
    status = serializers.IntegerField()