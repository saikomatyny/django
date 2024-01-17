import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import todolist, nameOfList
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

def getToDoList(request):
    todolist_objects = todolist.objects.all()
    name_of_list_objects = nameOfList.objects.all()
    
    todolist_values_dict = {}
    name_of_list_values_dict = {}

    for obj in todolist_objects:
        todolist_values_dict[obj.name_of_task] = obj.done_or_not

    values_list = []
    for name_of_list in name_of_list_objects:
        todolists = name_of_list.tasks.all()
        todolist_names = [todolist.name_of_task for todolist in todolists]
        name_of_list_values_dict[name_of_list.name_of_list] = todolist_names
        values_list += todolist_names

    common_values = list(set(todolist_values_dict.keys()).intersection(set(values_list)))
    
    for task in common_values:
        del todolist_values_dict[task]

    common_values = [todolist_values_dict, name_of_list_values_dict]
    all_tasks = {}

    for task in common_values:
        all_tasks.update(task)

    return JsonResponse(all_tasks, safe=False)

@api_view(['POST'])
def postToDoList(request):
    data = request.data

    try:
        if type(data) == list:
            for task in data:
                if 'name_of_task' in task:
                    if todolist.objects.filter(name_of_task=task['name_of_task']).exists():
                        duplicate = task['name_of_task']
                        return Response({'error': f'List already has {duplicate} task'}, status=status.HTTP_400_BAD_REQUEST)
                    
                    name_of_task = task['name_of_task']
                    done_or_not = task['done_or_not']
                    todolist.objects.create(name_of_task=name_of_task, done_or_not=done_or_not)
                else:
                    if nameOfList.objects.filter(name_of_list=task['name_of_list']).exists():
                        existing_list = nameOfList.objects.get(name_of_list=task['name_of_list'])
                        for lists in task['list_of_todo']:
                            if todolist.objects.filter(name_of_task=lists['name_of_task']).exists():
                                duplicate = lists['name_of_task']
                                return Response({'error': f'List already has {duplicate} task'}, status=status.HTTP_400_BAD_REQUEST)
                            temp = todolist.objects.create(name_of_task=lists['name_of_task'], done_or_not=lists['done_or_not'])
                            existing_list.tasks.add(temp)

                        return Response('Your data has been successfully added to server', status=status.HTTP_201_CREATED)
                    
                    new_list = nameOfList.objects.create(name_of_list=task['name_of_list'])
                    
                    for lists in task['list_of_todo']:
                        temp = todolist.objects.create(name_of_task=lists['name_of_task'], done_or_not=lists['done_or_not'])
                        temp.lists_of_todolist.add(new_list)
                    return Response('Your data has been successfully added to server', status=status.HTTP_201_CREATED)
        else:
            if todolist.objects.filter(name_of_task=data['name_of_task']).exists():
                duplicate = data['name_of_task']
                return Response({'error': f'List already has {duplicate} task'}, status=status.HTTP_400_BAD_REQUEST)
            
            name_of_task = data['name_of_task']
            done_or_not = data['done_or_not']

            todolist.objects.create(name_of_task=name_of_task, done_or_not=done_or_not)
        

        return Response('Your data has been successfully added to server', status=status.HTTP_201_CREATED)

    except KeyError as e:
        error_message = f'Missing key in data: {str(e)}'
        return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def deleteToDoList(request):
    data = request.data

    try:
        if type(data) == list:
            for name in data:
                try:
                    todolist.objects.get(name_of_task=name).delete()
                except:
                    error_message = f'There is no such task as {name}'
                    return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            todolist.objects.get(name_of_task=data).delete()
        
        return Response('Data has been successfully deleted from server', status=status.HTTP_201_CREATED)
    
    except KeyError as e:
        error_message = f'Missing name of task in data: {str(e)}'
        return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
    except todolist.DoesNotExist:
        return Response({'error' : f'{data} does not exist in list'})


def index(request):
    data = {
        'title': 'example #1',
        'main_text' : 'test test test',
        'list' : [1, 2, 3, '4', '5']
    }
    return render(request, 'main1/index.html', data)

def test(request):
    pass
