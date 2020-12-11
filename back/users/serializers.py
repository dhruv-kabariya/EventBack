from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import Student, Club, Membership


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name",
                  "email", "username", "avtar", "club"]

    def update(self, object, data):
        object.id = data.id
        object.first_name = data.first_name
        object.last_name = data.last_name
        object.email = data.email
        object.username = data.first_name + data.last_name
        object.avtar = data.avtar
        object.save()
        return object


class ClubSerializer(serializers.ModelSerializer):

    class Meta:
        model = Club
        fields = "__all__"


class MembershipSerializer(serializers.ModelSerializer):

    club = ClubSerializer()

    class Meta:

        model = Membership
        fields = ('club', 'position')


class OtherUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name", "avtar"]
