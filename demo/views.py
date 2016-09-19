from django.shortcuts import render
import orapp.models as models
from common_dibbs.clients.ar_client.apis.appliances_api import AppliancesApi
from settings import Settings
from common_dibbs.misc import configure_basic_authentication

def create_processdef(request):
    # appliances = AppliancesApi().appliances_get()
    return render(request, "processdef_form.html", {})


def create_processimpl(request):
    # Create a client for Appliances
    appliance_client = AppliancesApi()
    appliance_client.api_client.host = "%s" % (Settings().appliance_registry_url,)
    configure_basic_authentication(appliance_client, "admin", "pass")

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
