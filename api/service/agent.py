# coding=utf-8
import pickle
import hashlib
from datetime import datetime
import json
from random import randrange

from django.contrib.auth.models import User
from api.utils.exceptions.user import LoginAlredyExistException
from api.utils.exceptions.subscription import AgentLimitException
from rest_framework.exceptions import NotFound
from django.core.cache import cache

from api.models.agent import Agent
from api.models.purse import Purse
from api.models.user_group import UserGroup
from api.models.support import Support
from base_service import get_object, auth_user
from api.utils.exceptions.company import GroupNotFoundException, \
    AgentNotFoundException
from api.utils.exceptions.user import TokenOrCodeInvalidException
from api.utils.exceptions.auth import InvalidLoginException, InvalidPhoneException


def create_agent_start(serializer, request_user):
    company = Support.get_company_by_user(request_user)
    if company.agents_left < 1:
        raise AgentLimitException()

    if User.objects.filter(username=serializer.validated_data['login']).exists():
        raise LoginAlredyExistException()

    try:
        user_group = UserGroup.objects.get(id=serializer.validated_data['group_id'])
    except UserGroup.DoesNotExist:
        raise GroupNotFoundException()

    agent = serializer.create(serializer.validated_data, company, user_group)

    #TODO отправка смс сообщения с приглашением
    user_data = {'login': agent.user.username, 
                 'password': serializer.validated_data['password']}
    return user_data


def get_agent_by_id(id):
    try:
        agent = Agent.objects.get(id=id)
    except Agent.DoesNotExist:
        raise AgentNotFoundException()
    return agent


def delete_agent(agent):
    user = agent.user
    user.delete()


def update_agent(agent, serializer, group):
    old_login = agent.user.username
    new_login = serializer.validated_data['login']
    if (new_login != old_login) and (User.objects.filter(username=new_login).exists()):
        raise LoginAlredyExistException()

    serializer.update(agent, serializer.validated_data, group)


def get_agent_by_user(user):
    try:
        agent = Agent.get_agent_by_user(user)
    except Agent.DoesNotExist:
        raise AgentNotFoundException()
    return agent

def get_all_agents():
    return Agent.objects.all()

def is_first_auth(agent):
    return not bool(agent.platform)

def set_agent_device(agent, serializer, start_task):
    agent.device_id = serializer.validated_data['device_id']
    agent.platform = serializer.validated_data['platform']
    agent.save()

    company = agent.company
    screens = json.loads(company.screens)
    #TODO отправлять логотип при первом заходе или каждый раз?
    if start_task:
        start_task_id = start_task.task_addresses.get().id
    else:
        start_task_id = None
    data = {'screens': screens,
            'start_task_id': start_task_id}

    return data


def recover_password_start(form):
    phone = form.cleaned_data['phone']
    data = {}
    try:
        agent = Agent.objects.get(phone=phone)
    except Agent.DoesNotExist:
        raise InvalidPhoneException()

    code = str(randrange(9)) + str(randrange(9)) + str(randrange(9)) + str(randrange(9))
    #TODO несколько agent с одним телефоном
    token = hashlib.sha256(agent.user.username + str(datetime.now())).hexdigest()
    #TODO отправка кода подтверждения
    cache.set('{0}_{1}'.format(token, code), pickle.dumps(agent), 60*60*24)
    data['token'] = token
    data['code'] = code
    data['login'] = agent.user.username
    return data


def recover_password_finish(serializer):
    token = serializer.cleaned_data['token']
    password = serializer.cleaned_data['password']
    login = serializer.cleaned_data['login']
    code = serializer.cleaned_data['code']


    try:
        agent = pickle.loads(cache.get('{0}_{1}'.format(token, code)))
    except TypeError:
        raise TokenOrCodeInvalidException()

    if agent.user.username != login:
        raise InvalidLoginException()

    cache.delete('{0}_{1}'.format(token, code))
    agent.user.set_password(password)
    agent.user.save()

    return auth_user(login, password)