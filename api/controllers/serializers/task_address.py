# coding=utf-8
from rest_framework import serializers
from django.db import transaction

from api.models.task_address import TaskAddress


class TaskAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskAddress
        fields = ('id', 'task', 'longitude', 'latitude',
            'address', 'amount')


class TaskAddressCreateSerializer(serializers.Serializer):
    longitude = serializers.FloatField(default=None)
    latitude = serializers.FloatField(default=None)
    address = serializers.CharField(default=None)
    amount = serializers.IntegerField()
    id = serializers.IntegerField(default=0)


    def create(self, validated_data, task):
        task_address = TaskAddress(
            longitude = validated_data['longitude'],
            latitude=validated_data['latitude'],
            address=validated_data['address'],
            amount=validated_data['amount'],
            task=task)
        task_address.save()


    def update(self, task_address, validated_data):
        task_address.longitude = validated_data['longitude']
        task_address.latitude = validated_data['latitude']
        task_address.address = validated_data['address']
        task_address.amount = validated_data['amount']
        task_address.save()

    
class TaskWithoutAddressSerializer(serializers.ModelSerializer):


    title = serializers.CharField(source='task.title')
    client_name = serializers.CharField(source='task.client_name')
    price = serializers.IntegerField(source='task.price')
    description = serializers.CharField(source='task.description')
    start_dt = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", source='task.start_dt')
    finish_dt = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", source='task.finish_dt')


    class Meta:
        model = TaskAddress
        fields = ('id', 'title', 'client_name', 'price', 'description', 'start_dt', 'finish_dt')

class TaskWithAddressSerializer(TaskWithoutAddressSerializer):

    class Meta:
        model = TaskAddress
        fields = ('id', 'title', 'client_name', 'price', 'description', 'start_dt', 'finish_dt', \
            'latitude', 'longitude', 'address', 'distance')

