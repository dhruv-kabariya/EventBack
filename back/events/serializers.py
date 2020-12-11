from django.db.models import fields
from rest_framework import serializers

from events.models import Event, EventRegistraion
from users.models import Student

from users.serializers import OtherUserSerializer


class EventSerializer(serializers.ModelSerializer):

    class Meta:

        model = Event
        fields = "__all__"


class UserRegisterEventSerializer(serializers.ModelSerializer):

    class Meta:

        model = EventRegistraion
        fields = [
            "id",
            "evnetName",
            "attend"
        ]


class EventRegistraionSerializer(serializers.ModelSerializer):

    # eventName = serializers.ReadOnlyField(source= "eventName.name",read_only=True)
    class Meta:

        model = EventRegistraion
        fields = "__all__"

    def unform(self, data):

        exception_list = []
        eventName = data["event"]
        conformation = data["conformation"]
        list_of_user = data["users"]
        for i in list_of_user:
            try:
                user = EventRegistraion.objescts.get(
                    eventName=eventName, name=i)
                if user["conform"] != conformation:
                    user["conform"] = conformation
            except:
                exception_list.append(i)

            if len(exception_list) == 0:
                return {
                    "status": "error",
                    "error": "Some user was not in list",
                    "user": exception_list
                }
            else:
                return {
                    "status": "Success"
                }

    def attend(self, data):

        event = data["event"]
        user = data["user"]
        try:
            event = Event.objects.get(id=id)
            user = Studen.objects.get(username=user)
        except:
            return {
                "status": "fail",
                "error": "User or Event not found"
            }
        try:
            attendi = EventRegistraion.objects.get(evnetName=event, name=user)
            if attendi["attend"] == False:
                attendi["attend"] = True
                attendi.save()
                return attendi
            else:
                return {
                    "status": "fail",
                    "error": "User alredy checked"
                }
        except:
            return {
                "status": "fail",
                "error": "User does not have registred for event"
            }

    def registred(self, data):

        event = data["event"]
        user = data["user_id"]
        try:
            user = Student.objects.get(username=Student.objects.get(id=user))
        except:

            return {
                "status": "fail",
                "error": "User not found"
            }

        try:
            event = Event.objescts.get(eventName=Event.objescts.get(id=event))
        except:
            return {
                "status": "fail",
                "error": "Event not found"
            }

        register = EventRegistraion(
            name=user,
            eventName=event
        )
        register.save()
        return register


class EventRegistrationSerializer(serializers.ModelSerializer):

    name = OtherUserSerializer(read_only=True)

    class Meta:

        model = EventRegistraion
        fields = ["id", "evnetName", "name", "attend"]
