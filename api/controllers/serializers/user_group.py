# coding=utf-8
from rest_framework import serializers

from api.models.user_group import UserGroup


class UserGroupSerializer(serializers.ModelSerializer):
    '''
    Сериалайзер для модели UserGroup для получения связанных с ней 
    данных
    '''
    promos = serializers.CharField(source='promos.title')
    class Meta:
        model = UserGroup
        fields = ('id', 'name', 'support', 'promos')


class UserGroupCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    support_id = serializers.IntegerField()
    promo_id = serializers.IntegerField()
