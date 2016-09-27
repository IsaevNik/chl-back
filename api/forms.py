# coding: utf-8
from django import forms


class JsonReqForm(forms.Form):
    task = forms.CharField()

class UploadFileForm(forms.Form):
    content  = forms.FileField()

class TaskDistanceForm(forms.Form):
    latitude = forms.FloatField()
    longitude = forms.FloatField()
#   page = forms.IntegerField(required=False)

class RecoverPasswordSupportForm(forms.Form):
    email = forms.CharField()

class RecoverPasswordAgentStartForm(forms.Form):
    phone = forms.CharField()

class RecoverPasswordAgentFinishForm(forms.Form):
    login = forms.CharField()
    code = forms.CharField()
    password = forms.CharField()
    token = forms.CharField()