from companyservice.quickstart.serializers import CompanySerializer
from companyservice.quickstart.models import Company
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
import requests
import pika


from functools import wraps
import jwt
from django.http import JsonResponse

def get_token_auth_header(request):
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.META.get("HTTP_AUTHORIZATION", None)
    parts = auth.split()
    token = parts[1]

    return token

def requires_scope(required_scope):
    """Determines if the required scope is present in the Access Token
    Args:
        required_scope (str): The scope required to access the resource
    """
    def require_scope(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = get_token_auth_header(args[0])
            decoded = jwt.decode(token, verify=False)
            if decoded.get("scope"):
                token_scopes = decoded["scope"].split()
                for token_scope in token_scopes:
                    if token_scope == required_scope:
                        return f(*args, **kwargs)
            response = JsonResponse({'message': 'You don\'t have access to this resource'})
            response.status_code = 403
            return response
        return decorated
    return require_scope

@permission_classes([AllowAny])
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit'))
        channel = connection.channel()
        channel.queue_declare(queue='company_deletion_queue')
        message = f'User {instance.id} deleted'
        channel.basic_publish(exchange='', routing_key='company_deletion_queue', body=message)
        connection.close()

        self.perform_destroy(instance)


        return Response(status=status.HTTP_204_NO_CONTENT)

@permission_classes([AllowAny])
class EmailView(APIView):
    parser_classes=[JSONParser]

    def post(self, request):
        name = request.data.get('name', 'Quinn')
        email = request.data.get('email', '442982@student.fontys.nl')
        function_url = f"https://linkedtindermailingfunction.azurewebsites.net/api/mailfunction?name={name}&email={email}"
        response = requests.get(function_url)

        if response.status_code == 200:
            return Response({"message": response.text}, status=status.HTTP_200_OK)
        else:
            return Response(response.text, status=response.status_code)