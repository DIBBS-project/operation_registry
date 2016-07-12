from prapp.permissions import IsOwnerOrReadOnly

# Create your views here.

from django.contrib.auth.models import User
from prapp.models import ProcessDefinition, ProcessImplementation
from prapp.serializers import ProcessDefinitionSerializer, ProcessImplementationSerializer, UserSerializer
from rest_framework import viewsets, permissions, status

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'processdefs': reverse('processdef-list', request=request, format=format)
    })


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProcessDefViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = ProcessDefinition.objects.all()
    serializer_class = ProcessDefinitionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # Override to set the user using the credentials provided to perform the request + check the appliance.
    def create(self, request, *args, **kwargs):
        data2 = {}
        for key in request.data:
            data2[key] = request.data[key]
        data2[u'author'] = request.user.id
        data2[u'implementations'] = {}
        serializer = self.get_serializer(data=data2)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProcessImplViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = ProcessImplementation.objects.all()
    serializer_class = ProcessImplementationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # Override to set the user using the credentials provided to perform the request + check the appliance.
    def create(self, request, *args, **kwargs):
        from ar_client.apis.appliances_api import AppliancesApi
        try:
            AppliancesApi().appliances_name_get(request.data[u'appliance'])
        except:
            return Response('{"error": "Cannot retrieve appliance %s"}' % request.data[u'appliance'],
                            status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
        data2 = {}
        for key in request.data:
            if key == "process_definition":
                data2["process_definition"] = request.data[key]
            else:
                data2[key] = request.data[key]
        data2[u'author'] = request.user.id
        serializer = self.get_serializer(data=data2)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
