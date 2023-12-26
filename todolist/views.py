import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
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
    data = request.data

    try:
        if type(data) == list:
            for lists in data:
                name_of_task = lists['name_of_task']
                done_or_not = lists['done_or_not']
                todolists.objects.create(name_of_task=name_of_task, done_or_not=done_or_not)
        else:
            name_of_task = data['name_of_task']
            done_or_not = data['done_or_not']

            todolists.objects.create(name_of_task=name_of_task, done_or_not=done_or_not)
        

        return Response('Your data has been successfully added to server', status=status.HTTP_201_CREATED)

    except KeyError as e:
        error_message = f'Missing key in data: {str(e)}'
        return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)


def delete_endpoint(request):
    data = request.data

    try:
        if type(data) == list:
            for name in data:
                try:
                    todolists.objects.get(name_of_task=name).delete()
                except:
                    error_message = f'There is no such task as {name}'
                    return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            todolists.objects.get(name_of_task=name).delete()
        
        return Response('Data has been successfully deleted from server', status=status.HTTP_201_CREATED)
    
    except KeyError as e:
        error_message = f'Missing name of task in data: {str(e)}'
        return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

'''
def delete_endpoint(request):
    try:
        data = request.POST.getlist('name_of_task')
        if not data:
            raise KeyError("name_of_task")

        if isinstance(data, list):
            for name in data:
                try:
                    todolists.objects.get(name_of_task=name).delete()
                except todolists.DoesNotExist:
                    error_message = f'There is no such task as {name}'
                    return JsonResponse({'error': error_message}, status=400)
        else:
            try:
                todolists.objects.get(name_of_task=data).delete()
            except todolists.DoesNotExist:
                error_message = f'There is no such task as {data}'
                return JsonResponse({'error': error_message}, status=400)

        return JsonResponse({'message': 'Data has been successfully deleted from the server'}, status=200)
    except KeyError as e:
        error_message = f'Missing name_of_task in data: {str(e)}'
        return JsonResponse({'error': error_message}, status=400)
'''

def index(request):
    data = {
        'title': 'example #1',
        'main_text' : 'test test test',
        'list' : [1, 2, 3, '4', '5']
    }
    return render(request, 'main1/index.html', data)
