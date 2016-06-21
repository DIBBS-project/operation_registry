from django.shortcuts import render
import prapp.models as models
# from pdapp.prapp_client.apis import ProcessDefinitionsApi


def create_processdef(request):
    return render(request, "processdef_form.html")


# Index that provides a description of the API
def processes(request):

    processes = models.ProcessDefinition.objects.all()

    return render(request, "processes.html", {"processes": processes})
