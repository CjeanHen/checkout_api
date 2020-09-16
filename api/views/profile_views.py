from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.question import Profile
from ..serializers import ProfileSerializer, UserSerializer

# Create your views here.
class Profiles(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = ProfileSerializer
    def get(self, request):
        """Index request"""
        # Get all the mangos:
        # mangos = Mango.objects.all()
        # Filter the mangos by owner, so you can only see your owned mangos
        profiles = Profiles.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = ProfileSerializer(profiles, many=True).data
        return Response({ 'profiles': data })

    def post(self, request):
        """Create request"""
        # Add user to request data object
        request.data['profile']['owner'] = request.user.id
        # Serialize/create mango
        profile = ProfileSerializer(data=request.data['profile'])
        # If the mango data is valid according to our serializer...
        if profile.is_valid():
            # Save the created mango & send a response
            profile.save()
            return Response({ 'profile': question.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(profile.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):

    def partial_update(self, request, pk):
        """Update Request"""
        # Remove owner from request object
        # This "gets" the owner key on the data['mango'] dictionary
        # and returns False if it doesn't find it. So, if it's found we
        # remove it.
        if request.data['profile'].get('owner', False):
            del request.data['profile']['owner']

        # Locate Mango
        # get_object_or_404 returns a object representation of our Mango
        profile = get_object_or_404(Profile, pk=pk)
        # Check if user is the same as the request.user.id
        if not request.user.id == profile.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this profile')

        # Add owner to data object now that we know this user owns the resource
        request.data['profile']['owner'] = request.user.id
        # Validate updates with serializer
        data = ProfileSerializer(profile, data=request.data['profile'])
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
