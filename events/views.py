import base64
import datetime

from django.core.files.base import ContentFile
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins
from rest_framework.status import(
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED
)

from events.models import EventRegistraion, Event
from events.serializers import EventSerializer, EventRegistraionSerializer, EventRegistrationSerializer, UserRegisterEventSerializer

from users.models import Student, Club
# from users.models import Students


class EventView(APIView):

    permission_classes = [AllowAny, ]

    def get(self, request, format=None):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


class EventRegistartionView(APIView):

    permission_classes = [IsAuthenticated, ]

    def get_object(self, event):
        try:

            id = Event.objects.get(id=event).id
            return EventRegistraion.objects.filter(evnetName=id)
        except EventRegistraion.DoesNotExist:
            raise Http404

    def get(self, request, event, format=None):
        registered = self.get_object(event)
        serializer = EventRegistrationSerializer(registered, many=True)
        return Response(serializer.data)


class registerView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        event = request.data["event"]
        user = request.data["user_id"]

        try:
            user = Student.objects.get(id=user)
        except:

            return Response({
                "status": "fail",
                "error": "User not found"
            }, status=HTTP_404_NOT_FOUND)

        try:

            event = Event.objects.get(id=event)
        except:
            return Response({
                "status": "fail",
                "error": "Event not found"
            }, status=HTTP_404_NOT_FOUND)

        try:
            EventRegistraion.objects.get(name=user, evnetName=event)

            return Response(
                {
                    "Error": "Alredy registerded"
                },
                status=HTTP_400_BAD_REQUEST
            )

        except:

            register = EventRegistraion(
                name=user,
                evnetName=event
            )
            register.save()
            serialized = EventRegistrationSerializer(register)
            return Response(serialized.data,
                            status=HTTP_201_CREATED)


class EventAttendView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.data["user"]
        event = request.data["event"]
        attend = request.data["attend"]

        try:
            user = Student.objects.get(id=user)
            event = Event.objects.get(id=event)
        except:
            return Response(
                {"Error": "User or Event  not found"},
                status=HTTP_404_NOT_FOUND
            )

        try:

            attend = EventRegistraion.objects.get(evnetName=event, name=user)

        except:

            return Response(
                {"Error": "User is not registred"},
                status=HTTP_404_NOT_FOUND
            )

        if attend.conform == True:
            # print(attend.attend)
            if attend.attend != True:
                attend.attend = True
                attend.save()
                # print(attend.attend)
                data = EventRegistrationSerializer(attend).data

                return Response(
                    data,
                    status=HTTP_200_OK
                )
            else:
                return Response(
                    {"Error": "User is attending Event"},
                    status=HTTP_200_OK
                )

        else:
            return Response(
                {"Error": "User's Registration is not conformed"},
                status=HTTP_400_BAD_REQUEST
            )


class EventConformView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.data["user"]
        event = request.data["event"]

        try:
            user = Student.objects.get(id=user)
            event = Event.objects.get(id=event)
        except:
            return Response(
                {"Error": "User or Event  not found"},
                status=HTTP_404_NOT_FOUND
            )

        try:

            attend = EventRegistraion.objects.get(evnetName=event, name=user)

        except:

            return Response(
                {"Error": "User is not registred for event"},
                status=HTTP_404_NOT_FOUND
            )

        if attend.conform == False:
            attend.conform = True
            attend.save()

            data = EventRegistraionSerializer(attend).data

            return Response(
                data,
                status=HTTP_200_OK
            )
        else:
            return Response(
                {"Error": "User's Registration is not conformed"},
                status=HTTP_400_BAD_REQUEST
            )


class EventCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        if("poster" in data):

            image = data["poster"]
            name = data["name"]
            # print(image)
            if(';base64,' in image):
                format, imgstr = image.split(';base64,')

                ext = format.split('/')[-1]
            dataImage = ContentFile(base64.b64decode(
                image), name=name + str(datetime.datetime.now())+".jpeg")
            data["poster"] = dataImage
        data["club"] = Club.objects.get(id=int(request.data["club"]))

        event = Event(**data)
        event.save()
        data = EventSerializer(event).data
        return Response(
            data,
            status=HTTP_201_CREATED
        )


class EventEditView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        if("poster" in data):
            image = data["poster"]
            name = data["name"]
            if(';base64,' in image):
                format, imgstr = image.split(';base64,')
                ext = format.split('/')[-1]

            dataImage = ContentFile(base64.b64decode(
                image), name=name + str(datetime.datetime.now())+".jpeg")
            data["poster"] = dataImage

        event = Event.objects.get(id=data["id"])

        event.name = data["name"]
        if("poster" in data):
            event.poster = data["poster"]
        event.Description = data["Description"]
        event.venue = data["venue"]
        event.timeDate = data["timeDate"]
        event.club = Club.objects.get(id=int(data["club"]["id"]))
        event.save()

        data = EventSerializer(event).data
        return Response(
            data,
            status=HTTP_201_CREATED
        )


class UserRegisterEvent(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        data = UserRegisterEventSerializer(
            EventRegistraion.objects.filter(name=user.id), many=True)

        return Response(
            data.data,
            HTTP_200_OK
        )
