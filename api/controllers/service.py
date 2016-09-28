# coding=utf-8
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, \
    permission_classes, authentication_classes

from ..service.base_service import save_image
from api.permissions import IsCompanyStuff
from .renderers import JsonRenderer
from api.forms import UploadFileForm
from ..utils.exceptions.commons import RequestValidationException


@api_view(['POST'])
@renderer_classes([JsonRenderer])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsCompanyStuff])
def uploadImg(request):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        img_url = save_image(request.FILES['content'], request.user)
    else:
        raise RequestValidationException(form)

    return Response({'img_url': img_url})