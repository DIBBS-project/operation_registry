# coding: utf-8
from __future__ import absolute_import, print_function

from django.conf import settings
from django.shortcuts import render

from common_dibbs.clients.ar_client.apis.appliances_api import AppliancesApi
from common_dibbs.django import relay_swagger


import orapp.models as models


def create_processdef(request):
    # appliances = AppliancesApi().appliances_get()
    return render(request, "processdef_form.html", {})


def create_processimpl(request):
    # Create a client for Appliances
    appliance_client = AppliancesApi()
    appliance_client.api_client.host = settings.DIBBS['urls']['ar']
    relay_swagger(appliance_client, request)

    appliances = appliance_client.appliances_get()
    processdef_list = models.Operation.objects.all()
    return render(request, "processimpl_form.html", {"appliances": appliances, "processdefs": processdef_list})


# Index that provides a description of the API
def processdefs(request):
    processdef_list = models.Operation.objects.all()
    return render(request, "processdefs.html", {"processdefs": processdef_list})


# Index that provides a description of the API
def processimpls(request):
    processimpl_list = models.OperationVersion.objects.all()
    return render(request, "processimpls.html", {"processimpls": processimpl_list})
