from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.answer import Answer
from ..serializers import AnswerSerializer, UserSerializer

# Create your views here.
class Answers(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = AnswerSerializer
    def get(self, request):
        """Index request"""
        # Get all the mangos:
        # mangos = Mango.objects.all()
        # Filter the mangos by owner, so you can only see your owned mangos
        answers = Answers.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = AnswerSerializer(answers, many=True).data
        return Response({ 'answers': data })

    def post(self, request):
        """Create request"""
        # Add user to request data object
        request.data['answer']['owner'] = request.user.id
        # Serialize/create mango
        answer = AnswerSerializer(data=request.data['answer'])
        # If the mango data is valid according to our serializer...
        if answer.is_valid():
            # Save the created mango & send a response
            answer.save()
            return Response({ 'answer': answer.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(answer.errors, status=status.HTTP_400_BAD_REQUEST)

class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the mango to show
        answer = get_object_or_404(Answer, pk=pk)
        # Only want to show owned mangos?
        if not request.user.id == answer.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this answer')

        # Run the data through the serializer so it's formatted
        data = AnswerSerializer(answer).data
        return Response({ 'answer': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate mango to delete
        answer = get_object_or_404(Answer, pk=pk)
        # Check the mango's owner agains the user making this request
        if not request.user.id == answer.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this answer')
        # Only delete if the user owns the  mango
        answer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Remove owner from request object
        # This "gets" the owner key on the data['mango'] dictionary
        # and returns False if it doesn't find it. So, if it's found we
        # remove it.
        if request.data['answer'].get('owner', False):
            del request.data['answer']['owner']

        # Locate Mango
        # get_object_or_404 returns a object representation of our Mango
        question = get_object_or_404(Answer, pk=pk)
        # Check if user is the same as the request.user.id
        if not request.user.id == answer.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this answer')

        # Add owner to data object now that we know this user owns the resource
        request.data['answer']['owner'] = request.user.id
        # Validate updates with serializer
        data = AnswerSerializer(answer, data=request.data['answer'])
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
