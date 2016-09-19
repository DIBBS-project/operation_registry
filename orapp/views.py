from django.contrib.auth.models import User
from orapp.models import Operation, OperationVersion
from orapp.serializers import OperationSerializer, OperationVersionSerializer, UserSerializer
from common_dibbs.clients.ar_client.apis.appliances_api import AppliancesApi
from rest_framework import viewsets, permissions, status

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from settings import Settings
from common_dibbs.misc import configure_basic_authentication


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
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # Override to set the user using the credentials provided to perform the request + check the appliance.
    def create(self, request, *args, **kwargs):
        data2 = {}
        for key in request.data:
            data2[key] = request.data[key]
        data2[u'author'] = request.user.id
        data2[u'implementations'] = {}

        if data2[u'string_parameters'] == u'':
            data2[u'string_parameters'] = u'[]'

        if data2[u'file_parameters'] == u'':
            data2[u'file_parameters'] = u'[]'

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
    queryset = OperationVersion.objects.all()
    serializer_class = OperationVersionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # Override to set the user using the credentials provided to perform the request + check the appliance.
    def create(self, request, *args, **kwargs):
        try:
            # Create a client for Appliances
            appliance_client = AppliancesApi()
            appliance_client.api_client.host = "%s" % (Settings().appliance_registry_url,)
            configure_basic_authentication(appliance_client, "admin", "pass")

            appliance_client.appliances_name_get(request.data[u'appliance'])
        except:
            return Response('{"error": "Cannot retrieve appliance %s"}' % request.data[u'appliance'],
                            status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

        data2 = {u'script': u''}
        for key in request.data:
            data2[key] = request.data[key]

        data2[u'author'] = request.user.id

        if data2[u'output_parameters'] == u'':
            data2[u'output_parameters'] = u'{}'

        serializer = self.get_serializer(data=data2)
        serializer.is_valid(raise_exception=True)

        # Check that there are no extra variables (that all are declared in the process definition)
        from process_record import variables_set, files_set
        import json
        str_set = variables_set(data2[u'script'],
                                data2[u'output_type'],
                                json.loads(data2[u'output_parameters']))
        fil_set = files_set(data2[u'script'])

        process_definition = Operation.objects.get(id=data2[u'operation'])
        if process_definition.string_parameters:
            strs = json.loads(process_definition.string_parameters)
        else:
            strs = []
        if process_definition.string_parameters:
            fils = json.loads(process_definition.file_parameters)
        else:
            fils = []

        for e in str_set:
            if e not in strs:
                return Response(
                    '{"error": "String parameter \'%s\' not declared in the process definition \'%s\'"}'
                    % (e, process_definition.name),
                    status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
        for e in fil_set:
            if e not in fils:
                return Response(
                    '{"error": "File parameter \'%s\' not declared in the process definition \'%s\'"}'
                    % (e, process_definition.name),
                    status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
