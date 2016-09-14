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


