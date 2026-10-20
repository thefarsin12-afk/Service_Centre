from django.contrib.auth.models import User

from service.models import ServiceRequestModel

from rest_framework import serializers

import re

class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = ["id","username","email","password"]

        read_only_field = ["id"]

class ServiceRequestSerializer(serializers.ModelSerializer):

    problem_description = serializers.CharField(allow_blank=True)

    class Meta:

        model = ServiceRequestModel

        fields = "__all__"

        read_only_fields = ["id","created_date","user"] 

     

    def validate_vehicle_number(self,validate_data):

        pattern = r'^[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{4}$'

        validate_data = validate_data.strip().upper()

        if not re.fullmatch(pattern,validate_data):

            raise serializers.ValidationError(

                "Enter a valid vehicle number,e.g. KL08AB1234"
            )

        return validate_data

    def validate_problem_description(self,validate_data):

        if not validate_data or not validate_data.strip():

            raise serializers.ValidationError(

                "Problem description cannot be empty."
            )

        return validate_data.strip()