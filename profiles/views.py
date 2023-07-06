from rest_framework import status
from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
from DRF_prj.permissions import IsOwnerOrReadOnly

class ProfileList(APIView):
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True, context={'request': request})
        return Response(serializer.data)


class ProfileDetails(APIView):
    # Attribute of APIView that creates a form for the object
    serializer_class = ProfileSerializer
    # Attribute of APIView that allows to manage permissions
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
    # retrieve the object from the database
        try:
            profile = Profile.objects.get(pk=pk)
            # Call an method of APIView to check the permissions
            # If the user does not have permission, the method will
            # thrwo the 403 Error (Forbidden)
            self.check_object_permissions(self.request, profile)
            return profile
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
    # Handle the GET-Request
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
    # Handle the PUT-Request
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)
