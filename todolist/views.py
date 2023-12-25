import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import todolists
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

def get_endpoint(request):
    todolist_objects = todolists.objects.all()
    todolist_values_dict = {}

    for obj in todolist_objects:
        todolist_values_dict[obj.name_of_task] = obj.done_or_not

    return JsonResponse(todolist_values_dict)

@api_view(['POST'])
def post_endpoint(request):
    name_of_task = request.GET.get('name_of_task')
    done_or_not = request.GET.get('done_or_not')

    try:
        todolist_obj = todolists.objects.create(name_of_task=name_of_task, done_or_not=done_or_not)
        
        response_data = {
            'id': todolist_obj.id,
            'name_of_task': todolist_obj.name_of_task,
            'done_or_not': todolist_obj.done_or_not,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    except ValueError as e:
        error_message = f'Error creating Todolist object: {str(e)}'
        return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)


def index(request):
    data = {
        'title': 'example #1',
        'main_text' : 'test test test',
        'list' : [1, 2, 3, '4', '5']
    }
    return render(request, 'main1/index.html', data)
