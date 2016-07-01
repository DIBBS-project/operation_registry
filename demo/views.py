from django.shortcuts import render
import prapp.models as models
from prapp.ar_client.apis.appliances_api import AppliancesApi


def create_processdef(request):
    appliances = AppliancesApi().appliances_get()
    return render(request, "processdef_form.html", {"appliances": appliances})


# Index that provides a description of the API
def processdefs(request):
    processdef_list = models.ProcessDefinition.objects.all()
    return render(request, "processdefs.html", {"processdefs": processdef_list})
