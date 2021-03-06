# coding=utf-8
from django.contrib.auth.models import User
from rest_framework import serializers

from api.models.support import Support


class SupportListSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(source='user.email')
    company = serializers.CharField(source='company.name')

    class Meta:
        model = Support
        fields = ('id', 'name', 'email', 'company')


class SupportDetailSerializer(SupportListSerializer):
    '''
    Сериалайзер модели Support для получения 
    данных связанных с моделью
    '''
    name = serializers.CharField()
    role = serializers.SerializerMethodField()
    post = serializers.CharField(required=False)
    groups = serializers.SerializerMethodField() 

    class Meta:
        model = Support
        fields = ('id', 'name', 'email', 'company', 'role', 'post', 'groups')

    def get_role(self, obj):
        return obj.get_role_display()

    def get_groups(self, obj):
        data = []
        for group in obj.groups.all():
            data.append({'id': group.id, 'name': group.name})
        return data

    
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
            post=validated_data.get('post', ''),
            company=company)
        return support

    
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
        support.post = validated_data.get('post', '')
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
    email = serializers.CharField()
    password = serializers.CharField()