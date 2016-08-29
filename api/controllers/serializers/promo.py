# coding=utf-8
from rest_framework import serializers

from api.models.promo import Promo


class PromoSerializer(serializers.ModelSerializer):
    '''
    Сериалайзер для модели Promo для получения связанных с ней 
    данных
    '''
    class Meta:
        model = Promo
        fields = ('id', 'title', 'description', 'img_url', 'limit')


class PromoCreateSerializer(serializers.Serializer):
    '''
    Сериалайзер для создания поощрения
    '''
    title = serializers.CharField()
    description = serializers.CharField(required=False)
    img_url = serializers.CharField()
    limit = serializers.IntegerField()


