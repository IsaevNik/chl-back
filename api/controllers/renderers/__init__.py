# coding=utf-8
import json
import logging
from rest_framework.renderers import JSONRenderer
from rest_framework.views import exception_handler

#logger = logging.getLogger(__name__)


class JsonResponse:
    """
    ФОРМАТ ОТВЕТА API

    Успешный ответ:
        {
            'status': true,
            'data': {
                'user': user
            }
        }

    Не успешный ответ
        {
            'status': false,
            'error': {
                'exception': Exception,
                'message': message
            }
        }
    """
    def __init__(self, status, data=None, errors=None):
        self.status = status
        if data and not errors:
            self.data = data
        elif not data and errors:
            self.errors = errors
        elif data and errors:
            raise RuntimeError

    @staticmethod
    def success(data=None):
        return JsonResponse(True, data=data)

    @staticmethod
    def failure(e):
        return JsonResponse(False, errors={'exception': e.__class__.__name__, 'message': e.message})

    def json(self):
        return json.dumps(self.__dict__)


class JsonRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return JsonResponse.success(data=data).json()


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
#    logger.error(exc)
    if response is not None:
        response.content = JsonResponse.failure(exc).json()

    return response
