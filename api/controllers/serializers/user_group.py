# coding=utf-8
from rest_framework import serializers

from api.models.user_group import UserGroup


class UserGroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = ('id', 'name')

class UserGroupDetailSerializer(serializers.ModelSerializer):
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

    def create(self, validated_data, support, promo):
        UserGroup.objects.create(name=validated_data['name'],
                             support=support,
                             promos=promo)

    def update(self, group, validated_data, support, promo):
        group.support = support
        group.promo = promo
        group.name = validated_data['name']
        group.save()
