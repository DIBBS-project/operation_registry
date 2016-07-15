from rest_framework import serializers
from models import ProcessDefinition, ProcessImplementation
from django.contrib.auth.models import User


class ProcessDefinitionSerializer(serializers.ModelSerializer):
    implementations = serializers.PrimaryKeyRelatedField(many=True, queryset=ProcessImplementation.objects.all())

    class Meta:
        model = ProcessDefinition
        fields = ('id', 'name', 'author', 'argv', 'output_type', 'output_parameters', 'implementations')


class ProcessImplementationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessImplementation
        fields = ('id', 'name', 'process_definition', 'appliance', 'author', 'archive_url', 'creation_date', 'executable', 'cwd',
                  'environment')


class UserSerializer(serializers.ModelSerializer):
    process_definitions = serializers.PrimaryKeyRelatedField(many=True, queryset=ProcessDefinition.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'process_definitions')
