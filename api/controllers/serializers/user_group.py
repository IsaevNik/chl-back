# coding=utf-8
from rest_framework import serializers

from api.models.user_group import UserGroup


class UserGroupSerializer(serializers.ModelSerializer):
    '''
    Сериалайзер для модели UserGroup для получения связанных с ней 
    данных
    '''
    class Meta:
        model = UserGroup
        fields = ('name', 'support')


class UserGroupCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    support_id = serializers.IntegerField()
