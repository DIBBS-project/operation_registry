from django.shortcuts import render
import pdapp.models as models
from pdapp.prapp_client.apis import ProcessDefinitionsApi


def create_processdef(request):
    return render(request, "processdef_form.html")
