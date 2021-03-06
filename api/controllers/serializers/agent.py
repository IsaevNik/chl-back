# coding=utf-8
from django.contrib.auth.models import User
from rest_framework import serializers
from django.db import transaction

from api.models.agent import Agent
from api.models.user_group import UserGroup
from api.models.purse import Purse


class AgentListSerializer(serializers.ModelSerializer):
    '''
    Сериалайзер модели Agent для получения 
    данных связанных с моделью
    '''
    login = serializers.CharField(source='user.username')
    company = serializers.SerializerMethodField()
    platform = serializers.SerializerMethodField()

    class Meta:
        model = Agent
        fields = ('id', 'login', 'name', 'phone', 'company', 'platform')

    def get_platform(self,obj):
        return obj.get_platform_display()

    def get_company(self, obj):
        return {"id": obj.company.id, "name": obj.company.name}



class AgentDetailSerializer(AgentListSerializer):
    '''
    Сериалайзер модели Agent для получения 
    данных связанных с моделью
    '''
    balance = serializers.SerializerMethodField()


    class Meta:
        model = Agent
        fields = ('id', 'login', 'name', 'phone', 'company', 'group', \
                  'platform', 'post', 'device_id', 'balance')

    def get_balance(self, obj):
        return obj.purse.get_balance()

    def get_group(self, obj):
        return {"id": obj.group.id, "name": obj.group.name}


class GroupWithAgentsSerializer(serializers.ModelSerializer):
    '''
    Сериалайзер
    '''
    agents = AgentListSerializer(many=True, read_only=True)
    support = serializers.SerializerMethodField()

    class Meta:
        model = UserGroup
        fields = ('id', 'name', 'support','agents')

    def get_support(self, obj):
        return {"id": obj.support.id, "name": obj.support.name}

    
class CreateAgentStartSerializer(serializers.Serializer):
    '''
    Сериалайзер модели Agent для создания объектов
    класса Agent и обновления
    '''
    login = serializers.CharField()
    password = serializers.CharField()
    phone = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    group_id = serializers.IntegerField()
    post = serializers.CharField(required=False)

    def create(self, validated_data, company, user_group):
        user = User(
            username=validated_data['login'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'])
        user.save()
        user.set_password(validated_data['password'])
        user.save()
        agent = Agent(
            user=user,
            post=validated_data.get('post', ''),
            phone=validated_data['phone'],
            group=user_group,
            company=company)
        agent.save()
        purse = Purse()
        purse.agent = agent
        purse.save()
        return agent

    def update(self, agent, validated_data, group):
        a_user = agent.user
        a_user.username = validated_data['login']
        a_user.last_name = validated_data['last_name']
        a_user.first_name = validated_data['first_name']
        a_user.save()
        agent.post = validated_data.get('post','')
        agent.phone = validated_data['phone']
        agent.group = group
        agent.save()


class AuthAgentSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField()

class FirstAuthAgentSerializer(AuthAgentSerializer):
    platform = serializers.IntegerField()
    device_id = serializers.CharField()
