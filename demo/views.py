from django.shortcuts import render
import orapp.models as models
from orapp.ar_client.apis.appliances_api import AppliancesApi


def create_processdef(request):
    # appliances = AppliancesApi().appliances_get()
    return render(request, "processdef_form.html", {})


def create_processimpl(request):
    appliances = AppliancesApi().appliances_get()
    processdef_list = models.ProcessDefinition.objects.all()
    return render(request, "processimpl_form.html", {"appliances": appliances, "processdefs": processdef_list})


# Index that provides a description of the API
def processdefs(request):
    processdef_list = models.ProcessDefinition.objects.all()
    return render(request, "processdefs.html", {"processdefs": processdef_list})


# Index that provides a description of the API
def processimpls(request):
    processimpl_list = models.ProcessImplementation.objects.all()
    return render(request, "processimpls.html", {"processimpls": processimpl_list})
