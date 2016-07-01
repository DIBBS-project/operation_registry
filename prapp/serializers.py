from rest_framework import serializers
from models import ProcessDefinition
from django.contrib.auth.models import User


class ProcessDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessDefinition
        fields = ('id', 'name', 'author', 'appliance', 'archive_url', 'creation_date', 'executable', 'cwd',
                  'environment', 'argv', 'output_type', 'output_parameters')


class UserSerializer(serializers.ModelSerializer):
    process_definitions = serializers.PrimaryKeyRelatedField(many=True, queryset=ProcessDefinition.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'process_definitions')
