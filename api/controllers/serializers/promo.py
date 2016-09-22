# coding=utf-8
from rest_framework import serializers

from api.models.promo import Promo


class PromoListSerializer(serializers.ModelSerializer):
    '''
    Сериалайзер для модели Promo для получения связанных с ней 
    данных
    '''
    class Meta:
        model = Promo
        fields = ('id', 'title')


class PromoDetailSerializer(serializers.ModelSerializer):
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

    def create(self, validated_data, company):
        Promo.objects.create(title=validated_data['title'],
              description=validated_data.get('description', ''),
              img_url=validated_data['img_url'],
              limit=validated_data['limit'],
              company=company)

    def update(self, promo, validated_data):
        promo.title = validated_data['title']
        promo.description = validated_data.get('description', '')
        promo.img_url = validated_data['img_url']
        promo.limit = validated_data['limit']
        promo.save()