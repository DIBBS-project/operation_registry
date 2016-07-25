from rest_framework import serializers
from models import ProcessDefinition, ProcessImplementation
from django.contrib.auth.models import User


class ProcessDefinitionSerializer(serializers.ModelSerializer):
    implementations = serializers.PrimaryKeyRelatedField(many=True, queryset=ProcessImplementation.objects.all())

    class Meta:
        model = ProcessDefinition
        fields = ('id', 'name', 'logo_url', 'author', 'description', 'string_parameters', 'file_parameters', 'implementations')


class ProcessImplementationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessImplementation
        fields = ('id', 'name', 'author', 'process_definition', 'appliance', 'archive_url', 'creation_date',
                  'executable', 'cwd', 'environment', 'argv', 'output_type', 'output_parameters')


class UserSerializer(serializers.ModelSerializer):
    process_definitions = serializers.PrimaryKeyRelatedField(many=True, queryset=ProcessDefinition.objects.all())
    process_implementations = serializers.PrimaryKeyRelatedField(many=True, queryset=ProcessImplementation.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'process_definitions', 'process_implementations')
