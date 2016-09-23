# coding=utf-8
import pickle
import hashlib
from datetime import datetime
import json

from django.contrib.auth.models import User
from api.utils.exceptions.user import LoginAlredyExistException
from api.utils.exceptions.subscription import AgentLimitException
from rest_framework.exceptions import NotFound

from api.models.agent import Agent
from api.models.purse import Purse
from api.models.user_group import UserGroup
from api.models.support import Support
from base_service import get_object, auth_user
from api.utils.exceptions.company import GroupNotFoundException, \
    AgentNotFoundException


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
    print old_login, new_login
    if (new_login != old_login) and (User.objects.filter(username=new_login).exists()):
        raise LoginAlredyExistException

    serializer.update(agent, serializer.validated_data, group)


def get_agent_by_user(user):
    try:
        agent = Agent.get_agent_by_user(user)
    except Agent.DoesNotExist:
        raise NotFound()
    return agent

def get_all_agents():
    return Agent.objects.all()

def is_first_auth(agent):
    if agent.platform:
        return False
    else:
        return True

def set_agent_device(agent, serializer, start_task):
    agent.device_id = serializer.validated_data['device_id']
    agent.platform = serializer.validated_data['platform']
    agent.save()

    company = agent.company
    screens = json.loads(company.screens)
    #TODO отправлять логотип при первом заходе или каждый раз?

    start_task_id = start_task.id
    data = {'screens': screens,
            'start_task_id': start_task_id}

    return data