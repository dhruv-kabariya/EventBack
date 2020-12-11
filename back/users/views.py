import base64
import datetime

from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
    HTTP_200_OK, HTTP_502_BAD_GATEWAY

)
from rest_framework import parsers
from rest_framework.response import Response
from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Student, Club, Membership
from .serializers import StudentSerializer, MembershipSerializer, ClubSerializer


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("email")
    # print(username)
    password = request.data.get("password")
    if username is None or password is None:
        # print("credential")
        return Response({
            'error': 'Please provide both username and password',
        },
            status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response(
            {'error': 'Invalid credentials'},
            status=HTTP_400_BAD_REQUEST
        )

    token, _ = Token.objects.get_or_create(user=user)
    data = StudentSerializer(user).data
    if(data["club"] == True):
        try:
            mem = Membership.objects.get(name=data["id"])
            data["membership"] = MembershipSerializer(mem).data
        except:
            print("error")
            pass
    data["token"] = token.key
    return Response(
        data=data,
        status=HTTP_200_OK
    )


class Logout(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        return Response(status=HTTP_200_OK)


class Studentsignup(APIView):

    permission_classes = [AllowAny, ]

    def post(self, request):

        if("avtar" in request.data):
            image = request.data["avtar"]
            userName = request.data["username"]
            print(userName)
            if(';base64,' in image):
                format, image = image.split(';base64,')
                ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(
                image), name=userName + str(datetime.datetime.now())+".jpeg")
            request.data["avtar"] = data

        serialized = StudentSerializer(data=request.data)

        if serialized.is_valid():

            user = Student.objects.create(**request.data)
            user.set_password(request.data['password'])
            user.save()

            token, _ = Token.objects.get_or_create(user=user)
            data = StudentSerializer(user).data
            data["token"] = token.key
            return Response(
                data=data,
                status=HTTP_201_CREATED
            )
        else:
            return Response(
                serialized._errors,
                status=HTTP_400_BAD_REQUEST
            )


class StudentProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.data["user"]
        image = request.data["image"]

        format, imgstr = image.split(';base64,')
        ext = format.split('/')[-1]

        data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        user = Student.objects.get(id=user)
        user.avtar = data
        user.save()
        data = StudentSerializer(user).data
        return Response(
            data, status=HTTP_200_OK
        )

    def patch(self, request):

        user = Student.objects.get(id=request.data["id"])

        if("avtar" in request.data):
            image = request.data["avtar"]
            userName = request.data["username"]
            print(userName)
            if(';base64,' in image):
                format, image = image.split(';base64,')
                ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(
                image), name=userName + str(datetime.datetime.now())+".jpeg")
            request.data["avtar"] = data
        else:
            request.data["avtar"] = user.avtar

        serialized = StudentSerializer(data=request.data)
        if(serialized.is_valid()):
            id = Student.objects.update(**request.data)
            print(id)
        else:
            return Response(
                {"error": "Invalid"},
                status=HTTP_502_BAD_GATEWAY

            )
        data = StudentSerializer(data=Student.objects.get(id=id))
        return Response(
            data.data
        )


class ClubListView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        clubs = Club.objects.all()
        data = ClubSerializer(clubs, many=True).data
        return Response(
            data=data,
            status=HTTP_200_OK
        )
