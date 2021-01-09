from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions



class HelloApiView(APIView):
    """Test APIView"""
    serializer_class = serializers.HellloSerializer
    def get(self, request, format = None):
        """Returns a list of APIView features"""
        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'Is similiar to a traditional Django View',
            'Gives most control over application logic',
            'Is mapped manually to URLs',
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})

    def post(self, request):
        """Creates a hello message with our name"""
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            location = serializer.validated_data.get('location')
            phone = serializer.validated_data.get('phone')
            message = f'Hello {name} can you be in {location} by {phone}?'
            return Response({"message": message})
        else:
            return Response(
                serializer.errors,
                status= status.HTTP_400_BAD_REQUEST
            )
    def put(self, request, pk = None):
        """Handle updating an object"""
        return Response({"Method": "Put"})
    
    def patch(self, request, pk = None):
        """Partially updating an object"""
        return Response({"Method": "Patch"})

    def delete(self, request, pk = None):
        """Deleting an object"""
        return Response({"Method: Delete"})


class HelloViewSet(viewsets.ViewSet):
    """Test Api ViewSet"""
    serializer_class = serializers.HellloSerializer
    def list(self, request):
        """Return a hello Message"""
        a_viewset = [
            'Uses actions (List, Create, retrieve, update, partial_update',
            'Automatically maps to URLS using Routers',
            'Provides more functionality with less code',
        ]

        return Response({"Hello": "Hello", "a_viewset": a_viewset})

    def create(self, request):
        """Creates a new hello message"""
        serializer = self.serializer_class(data = request.data)  

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            location = serializer.validated_data.get('location')
            phone = serializer.validated_data.get('phone')  
            message = f'Hello {name} are you staying in {location} and is this your number{phone}?'
           
            return Response({"message": message})
        else:
            return Response(
                serializer.errors,
                status= status.HTTP_400_BAD_REQUEST
            )
    def retrieve(self, request, pk = None):
        """Handles getting object by it's ID"""
        return Response({"Method": "GET"})

    def update(self, request, pk = None):
        """Handle updating an object"""
        return Response({"Method": "PUT"})
    
    def partial_update(self, request, pk = None):
        """Handle removing an object"""
        return Response({"http_method": "PATCH"})

    def destroy(self, request, pk = None):
        """Handle Removing of an object"""
        return Response({"http_method": "DELETE"})

class UserProfileViewset(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)

class UserLoginApiView(ObtainAuthToken):
    """Handles creating users authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewset(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (
        permissions.UpdateOwnStatus,
        IsAuthenticatedOrReadOnly
    )

    def perform_create(self, serializer):
        serializer.save(user_profile = self.request.user)

