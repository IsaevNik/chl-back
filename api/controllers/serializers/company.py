# coding=utf-8
from rest_framework import serializers
from django.db import transaction

from api.models.company import Company


class CompanyFullSerializer(serializers.ModelSerializer):
    #TODO Добавить сведения о текущей подписке с датой окончания и тд.
    class Meta:
        model = Company
        fields = ('id', 'name', 'contact_person_first_name', 'contact_person_last_name',
            'contact_person_phone', 'address', 'logo_img', 'screen', 'invite_text', 
            'checking_acc', 'bank_name', 'ogrn', 'inn', 'kpp', 'ur_address', 'task_left')


class CompanyPartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ('id', 'name', 'logo_img', 'screen')

class RegCompanyStartSerializer(serializers.Serializer):
    name = serializers.CharField()
    contact_person_first_name = serializers.CharField()
    contact_person_last_name = serializers.CharField()
    email = serializers.EmailField()
    contact_person_phone = serializers.CharField()
    address = serializers.CharField()

    def create(self, validated_data):
        company = Company(
            name = validated_data['name'],
            contact_person_first_name=validated_data['contact_person_first_name'],
            contact_person_last_name=validated_data['contact_person_last_name'],
            contact_person_phone=validated_data['contact_person_phone'],
            address=validated_data['address'])

        return company

    def update():
        pass


class CompanyUpdateSerializer(serializers.Serializer):
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

        company.save()
