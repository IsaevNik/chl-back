# coding=utf-8
import pickle
import hashlib
from datetime import datetime

from api.controllers.serializers.support import CreateSupportStartSerializer
from api.controllers.serializers.company import CompanyFullSerializer
from django.contrib.auth.models import User
from django.core.cache import cache


def create_company_start(company_serializer):
    '''
    Создание компании
    '''
    if User.objects.filter(username=
                            company_serializer.validated_data['email']).exists():
        raise EmailAlreadyExistException

    company_data = company_serializer.validated_data
    support_data = {
        'email': company_data['email'],
        'first_name': company_data['contact_person_first_name'],
        'last_name': company_data['contact_person_last_name'],
        'role': 1,
        'post': ''
    }
    support_serializer = CreateSupportStartSerializer(data=support_data)

    company = company_serializer.create(company_data)
    support = support_serializer.create(support_data, company)

    token = hashlib.sha256(support.user.email + str(datetime.now())).hexdigest()

    cache.set(token, pickle.dumps(support), 60*60*24)

    return token

def update_company(company, serializer):
    #TODO write in log rewrite information
    serializer_for_write = CompanyFullSerializer(company)
    old_information = serializer_for_write.data

    serializer.update(company, serializer.validated_data)