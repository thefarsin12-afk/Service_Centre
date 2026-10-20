from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication,permissions
from rest_framework import serializers

from service.serializer import UserSerializer
from service.serializer import ServiceRequestSerializer
from service.models import ServiceRequestModel
from service.permission import IsOwned

class UserRegistrationView(APIView):

    def post(self,request):

        form_data = request.data

        serializer = UserSerializer(data=form_data)

        if serializer.is_valid():

            cleaned_data = serializer.validated_data

            qs = User.objects.create_user(**cleaned_data)

            serializer = UserSerializer(qs)

            return Response(data=serializer.data)

        else:
            return Response(data=serializer.errors)

    
class GetMeView(APIView):

    authentication_classes = [authentication.BasicAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        user = request.user

        qs = User.objects.get(username=user)

        serializer = UserSerializer(qs)

        return Response(data=serializer.data)        


class SeriviceRequestCreateList(APIView):

    authentication_classes = [authentication.BasicAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):

        form_data = request.data

        serializer = ServiceRequestSerializer(data=form_data)

        if serializer.is_valid():

            serializer.save(user=request.user)

            return Response(data=serializer.data)

        else:
            return Response(data=serializer.errors)


    def get(self,request):

        qs = ServiceRequestModel.objects.all()

        serializer = ServiceRequestSerializer(qs,many=True)

        return Response(data=serializer.data)

class ServiceRequestRetriveUpdateDelete(APIView):

    authentication_classes = [authentication.BasicAuthentication]

    permission_classes = [IsOwned]

    def get(self,request,pk=None):

        instance = get_object_or_404(ServiceRequestModel,id=pk)

        self.check_object_permissions(request,instance)

        serialize = ServiceRequestSerializer(instance)

        return Response(data=serialize.data)


    def put(self,request,pk=None):

        instance = get_object_or_404(ServiceRequestModel,id=pk)

        self.check_object_permissions(request,instance)

        form_data = request.data

        serializer = ServiceRequestSerializer(data=form_data,instance=instance)

        if serializer.is_valid():

            serializer.save()

            return Response (data=serializer.data)

        else:return Response(data=serializer.errors)

    def delete(self,request,pk=None):

        instance = get_object_or_404(ServiceRequestModel,id=pk)

        self.check_object_permissions(request,instance)

        instance.delete()

        return Response(data={"Message:Remowed"})

class FilterView(APIView):

    authentication_classes = [authentication.BasicAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        qs = ServiceRequestModel.objects.filter(user=request.user)

        service_type = request.query_params.get("service_type")

        priority = request.query_params.get("priority")

        status = request.query_params.get("status")

        if service_type:

            qs = qs.filter(service_type=service_type)

        if priority:

            qs = qs.filter(priority=priority)

        if status:

            qs = qs.filter(status=status)      

        serializer = ServiceRequestSerializer(qs,many=True)

        return Response(data=serializer.data)      


class SerachView(APIView):

    authentication_classes = [authentication.BasicAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def get(self,requset):

        qs = ServiceRequestModel.objects.filter(user=self.request.user)

        vehicle_number = requset.query_params.get("vehicle_number")

        vehicle_model = requset.query_params.get("vehicle_model")

        if vehicle_number:

            qs = qs.filter(vehicle_number__icontains = vehicle_number)

        if vehicle_model:

            qs = qs.filter(vehicle_model__icontains = vehicle_model)

        serializer = ServiceRequestSerializer(qs,many=True)

        return Response(data=serializer.data)

class PendingServiceView(APIView):

    authentication_classes = [authentication.BasicAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        qs = ServiceRequestModel.objects.filter(user=request.user,status="Requested")

        serilizer = ServiceRequestSerializer(qs,many=True)

        return Response(data=serilizer.data)

class SummaryServiceView(APIView):

    authentication_classes = [authentication.BasicAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        response_data = {

            "total_service":0
        }

        service_summary = ServiceRequestModel.objects.filter(user=request.user)

        if service_summary:

            total_service = service_summary.aggregate(total = Count("id")).get("total")

            status_wise = service_summary.values("status").annotate(total = Count("id"))

            response_data ["total_service"] = total_service
            
            response_data ["status_wise"] = status_wise

            return Response(data=response_data)

        else: serializers.ValidationError("No record")


class HighCriticalServiceView(APIView):

    authentication_classes = [authentication.BasicAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def get (self,request):

        qs = ServiceRequestModel.objects.filter(user = request.user,priority__in = ["High","Critical"])

        serializer = ServiceRequestSerializer(qs,many=True)

        return Response(data=serializer.data)
