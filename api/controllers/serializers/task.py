# coding=utf-8
from rest_framework import serializers
from django.db import transaction

from api.models.task import Task
from api.models.user_group import UserGroup
from task_address import TaskAddressSerializer
from point_blank import PointBlankSerializer


class TaskListSerializer(serializers.ModelSerializer):
    task_addresses = serializers.IntegerField(source='task_adresses_count')

    class Meta:
        model = Task
        fields = ('id', 'client_name', 'title', 'task_addresses')

class TaskDetailSerializer(serializers.ModelSerializer):

    last_editor = serializers.CharField(source='last_editor.name')
    creater = serializers.CharField(source='creater.name')
    task_addresses = TaskAddressSerializer(many=True, read_only=True)
    blanks = PointBlankSerializer(many=True, read_only=True)
    finish_dt = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    start_dt = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    release_dt = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    create_dt = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    last_edit_dt = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Task
        fields = ('id', 'client_name', 'title', 'description',
            'creater', 'last_editor', 'price', 'start_dt', 'finish_dt', 
            'release_dt', 'create_dt', 'last_edit_dt', 'is_start', 
            'blanks', 'task_addresses')


class GroupWithTaskSerializer(serializers.ModelSerializer):

    tasks = TaskListSerializer(many=True, read_only=True)
    group_name = serializers.CharField(source='name')
    class Meta:
        model = UserGroup
        fields = ('id', 'group_name', 'tasks')


class TaskCreateSerializer(serializers.Serializer):
    client_name = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    price = serializers.IntegerField()
    start_dt = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    finish_dt = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    is_start = serializers.IntegerField(default=0)
    group_id = serializers.IntegerField(required=False, allow_null=True)


    def create(self, validated_data, support, group):
        task = Task(
            client_name = validated_data['client_name'],
            title=validated_data['title'],
            description=validated_data['description'],
            price=validated_data['price'],
            start_dt=validated_data['start_dt'],
            finish_dt=validated_data['finish_dt'],
            is_start=bool(validated_data['is_start']),
            creater=support,
            last_editor=support,
            group=group)
        task.save()
        return task


    def update(self, task, validated_data, support, group):
        task.client_name = validated_data['client_name']
        task.title = validated_data['title']
        task.description = validated_data['description']
        task.price = validated_data['price']
        task.start_dt = validated_data['start_dt']
        task.finish_dt = validated_data['finish_dt']
        task.last_editor = support
        task.group = group
        task.save()
        return task

