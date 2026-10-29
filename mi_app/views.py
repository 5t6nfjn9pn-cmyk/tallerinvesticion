# LIBRERIAS
import json
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from .models import Proyecto


# VISTA
@method_decorator(csrf_exempt, name='dispatch')
class ProyectoView(View):

    # READ: lista todos o devuelve uno si llega pk
    def get(self, request, pk=None):
        if pk is not None:
            proyecto = get_object_or_404(Proyecto, pk=pk)
            return JsonResponse(model_to_dict(proyecto))
        proyectos = list(Proyecto.objects.values())
        return JsonResponse(proyectos, safe=False)

    # CREATE
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON invalido'}, status=400)

        if not data.get('nombre'):
            return JsonResponse({'error': 'El campo nombre es obligatorio'}, status=400)

        proyecto = Proyecto.objects.create(
            nombre=data['nombre'],
            descripcion=data.get('descripcion', '')
        )
        return JsonResponse(model_to_dict(proyecto), status=201)

    # UPDATE
    def put(self, request, pk):
        proyecto = get_object_or_404(Proyecto, pk=pk)
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON invalido'}, status=400)

        proyecto.nombre = data.get('nombre', proyecto.nombre)
        proyecto.descripcion = data.get('descripcion', proyecto.descripcion)
        proyecto.save()
        return JsonResponse(model_to_dict(proyecto))

    # DELETE
    def delete(self, request, pk):
        proyecto = get_object_or_404(Proyecto, pk=pk)
        proyecto.delete()
        return HttpResponse(status=204)