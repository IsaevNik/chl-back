# coding=utf-8
#from rest_framework.authentication import TokenAuthentication
#from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class CompanyView(APIView):
    
    authentication_classes = ()
    permission_classes = (IsAdminOrReadOnly,)
    renderer_classes = (JsonRenderer,)

    def get(request):
        return Render()

    def put(request):
        return Render()


class RegCompany

    authentication_classes = ()
    permission_classes = ()
    renderer_classes = (JsonRenderer,)

    def post(request):
        return Render()