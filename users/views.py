from django.shortcuts import render, redirect
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth import authenticate, logout as django_logout, login as django_login
import json
import secrets
import string
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.http import HttpResponse, JsonResponse

# Create your views here.

def login(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        try:
            user = User.objects.get(email=body['email'])
            if user.check_password(body['password']):
                token = Token.objects.get_or_create(user=user)[0]
                data = {
                    'user_id': user.id,
                    'email': user.email,
                    'status': 'success',
                    'token': str(token),
                    'code': status.HTTP_200_OK,
                    'message': 'Login successfull',
                    'data': []
                }
                dump = json.dumps(data)
                return HttpResponse(dump, content_type='application/json')
            else:
                data = {
                    'status': 'failure',
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Phone or password incorrect!',
                    'data': []
                }
                dump = json.dumps(data)
                return HttpResponse(dump, content_type='application/json')
        except User.DoesNotExist:
            data = {
                'status': 'failure',
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Phone or password incorrect!',
                'data': []
            }
            dump = json.dumps(data)
            return HttpResponse(dump, content_type='application/json')


def logout(request):
    if request.method == 'POST':
        django_logout(request)
    return redirect('login')



class usersListView(ListAPIView):
    serializer_class = UserSerializer
    def get_queryset(self):
        return User.objects.all()


class clientsListView(ListAPIView):
    serializer_class = ClientSerializer
    def get_queryset(self):
        return Client.objects.all()

class firmsListView(ListAPIView):
    serializer_class = FirmSerializer
    def get_queryset(self):
        return Firm.objects.all()

class lawyersListView(ListAPIView):
    serializer_class = LawyerSerializer
    def get_queryset(self):
        return Lawyer.objects.all()

class casesListView(ListAPIView):
    serializer_class = CaseSerializer
    def get_queryset(self):
        return Case.objects.all()


class register_client(CreateAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def create(self, request):
        body_unicode=request.body.decode('utf-8')
        body=json.loads(body_unicode)
        print(body)
        # alphabet = string.ascii_letters + string.digits
        # password = ''.join(secrets.choice(alphabet) for i in range(6))
        try:
            user_ = User.objects.get(email=body['email'])
            response = {
                'status': 'Failure',
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'A user with that email already exists!',
                'data': []
            }

            return Response(response)
        except User.DoesNotExist:
            user = User.objects.create_user(
                    email=body['email'],
                    user_type='client',
                    password=body['password'])
            
            client = Client()
            client.user = user
            client.name=body['name']
            client.phone=body['phone']
            client.address=body['address']
            client.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'client created successfully!!!',
                'data': []
            }

            return Response(response)



class register_firm(CreateAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def create(self, request):
        body_unicode=request.body.decode('utf-8')
        body=json.loads(body_unicode)
        print(body)
        # alphabet = string.ascii_letters + string.digits
        # password = ''.join(secrets.choice(alphabet) for i in range(6))
        try:
            user_ = User.objects.get(email=body['email'])
            response = {
                'status': 'Failure',
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'A user with that email already exists!',
                'data': []
            }

            return Response(response)
        except User.DoesNotExist:
            user = User.objects.create_user(
                    email=body['email'],
                    user_type='firm',
                    password=body['password'])
            
            client = Firm()
            client.user = user
            client.name=body['name']
            client.phone=body['phone']
            client.address=body['address']
            client.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Firm registered successfully!!!',
                'data': []
            }

            return Response(response)




class register_lawyer(CreateAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def create(self, request):
        body_unicode=request.body.decode('utf-8')
        body=json.loads(body_unicode)
        print(body)
        # alphabet = string.ascii_letters + string.digits
        # password = ''.join(secrets.choice(alphabet) for i in range(6))
        try:
            user_ = User.objects.get(email=body['email'])
            response = {
                'status': 'Failure',
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'A user with that email already exists!',
                'data': []
            }

            return Response(response)
        except User.DoesNotExist:
            user = User.objects.create_user(
                    email=body['email'],
                    user_type='lawyer',
                    password=body['password'])
            firm = Firm.objects.get(id=str(body['firm']))
            client = Lawyer()
            client.user = user
            client.firm = firm
            client.name=body['name']
            client.phone=body['phone']
            client.address=body['address']
            client.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Lawyer registered successfully!!!',
                'data': []
            }

            return Response(response)


class add_case(CreateAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

# class add_case(CreateAPIView):
#     parser_classes = (MultiPartParser, FormParser, JSONParser)
#     serializer_class = CaseSerializer
#     def create(self, request):
#         body_unicode=request.body.decode('utf-8')
#         body=json.loads(body_unicode)
#         print(request.body)
#         firm = Firm.objects.get(id=str(body['firm']))
#         client = Client.objects.get(id=str(body['client']))
#         case = Case()
#         case.client = client
#         case.firm = firm
#         case.subject=body['subject']
#         case.area=body['area']
#         case.proof=body['proof']
#         case.save()
#         response = {
#             'status': 'success',
#             'code': status.HTTP_200_OK,
#             'message': 'Case added successfully!!!',
#             'data': []
#         }

#         return Response(response)