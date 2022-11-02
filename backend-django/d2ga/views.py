from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers

class SwaggerSchemaView(APIView):
    """
    Use this endpoint to view API documentation.
    """
    permission_classes = [IsAdminUser]
    renderer_classes = [
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]
    authentication_classes = [SessionAuthentication]

    def get(self, request):
        generator = SchemaGenerator()
        schema = generator.get_schema()

        return Response(schema)
