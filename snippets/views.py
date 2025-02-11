from snippets.models import Snippet
from snippets.permissions import IsOwnerOrReadOnly
from snippets.serializers import SnippetSerializer, UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import action
from knox.views import LoginView as KnoxLoginView
from rest_framework.authentication import BasicAuthentication
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope


class LoginAPI(KnoxLoginView):
    authentication_classes = [BasicAuthentication]

class ApiRoot(generics.GenericAPIView):
    """
    API root view.
    """
    def get(self, request, format=None, *args, **kwargs):
        return Response({
            'users': reverse('user-list', request=request, format=format),
            'snippets': reverse('snippet-list', request=request, format=format)
        })


class SnippetViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly] #, TokenHasReadWriteScope]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['users']
