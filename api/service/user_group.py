# coding=utf-8
from rest_framework.exceptions import NotFound

from api.models.support import Support
from api.models.user_group import UserGroup
from support import get_support
from base_service import get_object


def create_group(serializer, user):
	support = get_support(serializer.validated_data['support_id'], user)
	UserGroup.objects.create(name=serializer.validated_data['name'],
							 support=support)

def get_all_groups_of_company(user):
	company = Support.get_company_by_user(user)
	groups = UserGroup.objects.filter(support__company=company)
	return groups

def get_group(id, user):
	company = Support.get_company_by_user(user)
	group = get_object(UserGroup, id)
	if group.support.company != company:
		raise NotFound()
	return group

def update_group(group, serializer, user):
	support = get_support(serializer.validated_data['support_id'], user)
	group.support = support
	group.name = serializer.validated_data['name']
	group.save()

def delete_group(group):
	group.delete()