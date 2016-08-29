# coding=utf-8
from django.contrib.auth.models import User
from rest_framework import serializers
from django.db import transaction

from api.models.support import Support


class SupportSerializer(serializers.ModelSerializer):
    '''
    Сериалайзер модели Support для получения 
    данных связанных с моделью
    '''
    name = serializers.CharField()
    email = serializers.EmailField(source='user.email')
    role = serializers.SerializerMethodField()
    post = serializers.CharField(required=False)  

    class Meta:
        model = Support
        fields = ('id', 'name', 'email', 'company', 'role', 'post')

    def get_role(self,obj):
        return obj.get_role_display()

    
class CreateSupportStartSerializer(serializers.Serializer):
    '''
    Сериалайзер модели Support для создания объектов
    класса Support и обновления
    '''
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    role = serializers.IntegerField(default=2)
    post = serializers.CharField(required=False)

    def create(self, validated_data, company):
        user = User(
            email=validated_data['email'],
            username=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'])
        support = Support(
            user=user,
            role=validated_data['role'],
            post=validated_data['post'],
            company=company)
        return support

    @transaction.atomic
    def update(self, support, validated_data):
        s_user = support.user
        s_user.username = validated_data['email']
        s_user.email = validated_data['email']
        s_user.last_name = validated_data['last_name']
        s_user.first_name = validated_data['first_name']
        s_user.save()

        #if support.is_admin and validated_data['role'] == 2:
        #    raise ChangeAdminToSupportException
        support.role = validated_data['role']
        support.post = validated_data['post']
        support.save()


class CreateSupportFinishSerializer(serializers.Serializer):
    '''
    Сериализатор для завершения создания оператора
    '''
    email = serializers.EmailField()
    password = serializers.CharField()
    token = serializers.CharField()


class AuthSupportSerializer(serializers.Serializer):
    """
    Сериализатор для авторизации Оператора
    """
    def create(self, validated_data):
        raise RuntimeError("Wrong usage %s" % self.__class__.__name__)

    def update(self, instance, validated_data):
        raise RuntimeError("Wrong usage %s" % self.__class__.__name__)

    email = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100)