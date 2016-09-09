# coding=utf-8
import pickle
import hashlib
from datetime import datetime
import json

from django.contrib.auth.models import User
from api.utils.exceptions.user import LoginAlredyExistException
from api.utils.exceptions.company import AgentLimitException
from rest_framework.exceptions import NotFound

from api.models.agent import Agent
from api.models.user_group import UserGroup
from api.models.support import Support
from base_service import get_object, auth_user
from ..service.task import get_start_task_by_company


def create_agent_start(serializer, request_user):
    company = Support.get_company_by_user(request_user)
    if company.agents_left < 1:
        raise AgentLimitException

    if User.objects.filter(username=serializer.validated_data['login']).exists():
        raise LoginAlredyExistException

    try:
        user_group = UserGroup.objects.get(id=serializer.validated_data['group_id'])
    except UserGroup.DoesNotExist:
        raise NotFound

    agent = serializer.create(serializer.validated_data, company, user_group)
    user_data = {'login': agent.user.username, 
                 'password': serializer.validated_data['password']}
    return user_data


def get_agent(id, user):
    company = Support.get_company_by_user(user)
    agent = get_object(Agent, id)
    if agent.company != company:
        raise NotFound()
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

def set_agent_device(agent, serializer):
    agent.device_id = serializer.validated_data['device_id']
    agent.platform = serializer.validated_data['platform']
    agent.save()

    company = agent.company
    screens = json.loads(company.screen)
    #TODO отправлять логотип при первом заходе или каждый раз?

    start_task = get_start_task_by_company(company)
    start_task_id = start_task.id
    data = {'screen': screens,
            'start_task_id': start_task_id}

    return data