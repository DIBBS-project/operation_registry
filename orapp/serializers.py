# coding: utf-8
from __future__ import absolute_import

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Operation, OperationVersion


class OperationSerializer(serializers.ModelSerializer):
    implementations = serializers.PrimaryKeyRelatedField(many=True, queryset=OperationVersion.objects.all())

    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # def validate_author(self, author):
    #     UserModel = get_user_model()
    #     return UserModel.objects.get(username=author)

    class Meta:
        model = Operation
        fields = ('id', 'name', 'logo_url', 'author', 'description', 'string_parameters', 'file_parameters',
                  'implementations')


class OperationVersionSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # def validate_author(self, author):
    #     UserModel = get_user_model()
    #     return UserModel.objects.get(username=author)

    class Meta:
        model = OperationVersion
        fields = ('id', 'name', 'author', 'operation', 'appliance', 'creation_date', 'cwd', 'script',
                  'output_type', 'output_parameters')


# class UserSerializer(serializers.ModelSerializer):
#     operations = serializers.PrimaryKeyRelatedField(many=True,
#                                                     queryset=Operation.objects.all())
#     operation_versions = serializers.PrimaryKeyRelatedField(many=True,
#                                                             queryset=OperationVersion.objects.all())
#
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'operations', 'operation_versions')
