# coding: utf-8
from django import forms


class JsonReqForm(forms.Form):
    task = forms.CharField()
