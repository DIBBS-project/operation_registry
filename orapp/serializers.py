from rest_framework import serializers
from models import Operation, OperationVersion
from django.contrib.auth.models import User


class OperationSerializer(serializers.ModelSerializer):
    implementations = serializers.PrimaryKeyRelatedField(many=True, queryset=OperationVersion.objects.all())

    class Meta:
        model = Operation
        fields = ('id', 'name', 'logo_url', 'author', 'description', 'string_parameters', 'file_parameters',
                  'implementations')


class OperationVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationVersion
        fields = ('id', 'name', 'author', 'operation', 'appliance', 'creation_date', 'cwd', 'script',
                  'output_type', 'output_parameters')


class UserSerializer(serializers.ModelSerializer):
    operations = serializers.PrimaryKeyRelatedField(many=True,
                                                    queryset=Operation.objects.all())
    operation_versions = serializers.PrimaryKeyRelatedField(many=True,
                                                            queryset=OperationVersion.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'operations', 'operation_versions')
