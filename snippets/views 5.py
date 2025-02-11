from snippets.models import Snippet
from snippets.permissions import IsOwnerOrReadOnly
from snippets.serializers import SnippetSerializer, UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import renderers


class ApiRoot(generics.GenericAPIView):
    """
    API root view.
    """
    def get(self, request, format=None, *args, **kwargs):
        return Response({
            'users': reverse('user-list', request=request, format=format),
            'snippets': reverse('snippet-list', request=request, format=format)
        })

class SnippetList(generics.ListCreateAPIView):
    """
    List all snippets, or create a new snippet.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)