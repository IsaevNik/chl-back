from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework import response, schemas
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer


@api_view()
@permission_classes([])
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Checklines API/web')
    return response.Response(generator.get_schema(request=request))