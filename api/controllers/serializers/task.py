# coding=utf-8
from rest_framework import serializers
from django.db import transaction

from api.models.task import Task


class TaskSerializer(serializers.ModelSerializer):

    last_editor = serializers.CharField(source='last_editor.name')
    creater = serializers.CharField(source='creator.name')
    group = serializers.CharField(source='group.name')
    class Meta:
        model = Task
        fields = ('id', 'client_name', 'title', 'description',
            'creater', 'last_editor', 'price', 'start_dt', 'finish_dt', 
            'release_dt', 'create_dt', 'last_edit_dt', 'execute_dt', 'is_start')


class TaskCreateSerializer(serializers.Serializer):
    client_name = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    price = serializers.IntegerField()
    start_dt = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    finish_dt = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    is_start = serializers.IntegerField(default=0)
    group_id = serializers.IntegerField(required=False)


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


    def update():
        pass


'''class CompanyUpdateSerializer(serializers.Serializer):
    name = serializers.CharField()
    contact_person_first_name = serializers.CharField()
    contact_person_last_name = serializers.CharField()
    contact_person_phone = serializers.CharField()
    address = serializers.CharField()
    logo_img = serializers.CharField()
    screen = serializers.CharField()
    invite_text = serializers.CharField()
    checking_acc =  serializers.CharField()
    bank_name = serializers.CharField()
    ogrn = serializers.CharField()
    inn = serializers.CharField()
    kpp = serializers.CharField()
    ur_address = serializers.CharField()

    def update(self, company, validated_data):
        company.name = validated_data['name']
        company.contact_person_first_name = validated_data['contact_person_first_name']
        company.contact_person_last_name = validated_data['contact_person_last_name']
        company.contact_person_phone = validated_data['contact_person_phone']
        company.address = validated_data['address']
        company.logo_img = validated_data['logo_img']
        company.screen = validated_data['screen']
        company.invite_text = validated_data['invite_text']
        company.checking_acc = validated_data['checking_acc']
        company.bank_name = validated_data['bank_name']
        company.ogrn = validated_data['ogrn']
        company.inn = validated_data['inn']
        company.kpp = validated_data['kpp']
        company.ur_address = validated_data['ur_address']

        company.save()'''
