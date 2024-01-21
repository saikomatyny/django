import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import todolist, nameOfList
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

def getToDoList(request):
    todolist_objects = todolist.objects.all()
    name_of_list_objects = nameOfList.objects.all()
    
    todolist_values_dict = {}
    name_of_list_values_dict = {}

    for obj in todolist_objects:
        todolist_values_dict[obj.name_of_task] = {'done_or_not' : obj.done_or_not, 'date' : obj.date_field}

    values_list = []
    for name_of_list in name_of_list_objects:
        todolists = name_of_list.tasks.all()
        todolist_names = {}
        for todolist_ in todolists:
            todolist_names[todolist_.name_of_task] = {'done_or_not' : todolist_.done_or_not, 'date' : todolist_.date_field}
            
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

'''
Example for post endpoint
[
  {"name_of_list": "list1", "list_of_todo": [{"name_of_task": "Task1", "date" : "now"}]},
  {"name_of_list": "list2", "list_of_todo": [{"name_of_task": "Task2", "date" : "now"}]},
  {"name_of_task": "Task3", "date": "2022-01-17T12:30:00"},
  {"name_of_task": "Task4"} #in this case {{date_field}} will equal current UTC date and time
]
'''




@api_view(['POST'])
def postToDoList(request):
    data = request.data

    def dateParse(lst):
        temp_arr = lst['date'].split('T')
        res_date = [temp_arr[0].split('-')]
        res_date += [temp_arr[1].split(':')]
        return res_date
    #test_str = ''
    try:
        if type(data) == list:
            for task in data:
                
                if 'name_of_task' in task:
                    #test_str += '1'
                    if todolist.objects.filter(name_of_task=task['name_of_task']).exists():
                        duplicate = task['name_of_task']
                        #test_str += '2'
                        return Response({'error': f'List already has {duplicate} task'}, status=status.HTTP_400_BAD_REQUEST)
                    
                    if 'date' not in task or task['date'].lower() == 'now':
                        new_task = todolist.objects.create(name_of_task=task['name_of_task'], done_or_not=False, date_field = datetime.now())
                    else:
                        res_date = dateParse(task)
                        new_task = todolist.objects.create(name_of_task=task['name_of_task'], done_or_not=False, date_field = datetime(int(res_date[0][0]), int(res_date[0][1]), int(res_date[0][2]), int(res_date[1][0]), int(res_date[1][1]), int(res_date[1][2])))
                else:
                    #test_str += '3'
                    if nameOfList.objects.filter(name_of_list=task['name_of_list']).exists():
                        existing_list = nameOfList.objects.get(name_of_list=task['name_of_list'])
                        for lists in task['list_of_todo']:
                            if todolist.objects.filter(name_of_task=lists['name_of_task']).exists():
                                duplicate = lists['name_of_task']
                                #test_str += '4'
                                return Response({'error': f'List already has {duplicate} task'}, status=status.HTTP_400_BAD_REQUEST)
                            if 'date' not in lists or lists['date'].lower() == 'now':
                                new_task = todolist.objects.create(name_of_task=lists['name_of_task'], done_or_not=False, date_field = datetime.now())
                            else:
                                res_date = dateParse(lists)
                                new_task = todolist.objects.create(name_of_task=lists['name_of_task'], done_or_not=False, date_field = datetime(int(res_date[0][0]), int(res_date[0][1]), int(res_date[0][2]), int(res_date[1][0]), int(res_date[1][1]), int(res_date[1][2])))
                            existing_list.tasks.add(new_task)
                    else:
                        new_list = nameOfList.objects.create(name_of_list=task['name_of_list'])
                        #test_str += '5'
                        for lists in task['list_of_todo']:
                            if todolist.objects.filter(name_of_task=lists['name_of_task']).exists():
                                    #test_str += '6'
                                    duplicate = lists['name_of_task']
                                    return Response({'error': f'List already has {duplicate} task'}, status=status.HTTP_400_BAD_REQUEST)
                            if 'date' not in lists or lists['date'].lower() == 'now':
                                new_task = todolist.objects.create(name_of_task=lists['name_of_task'], done_or_not=False, date_field = datetime.now())
                            else:
                                res_date = dateParse(lists)
                                new_task = todolist.objects.create(name_of_task=lists['name_of_task'], done_or_not=False, date_field = datetime(int(res_date[0][0]), int(res_date[0][1]), int(res_date[0][2]), int(res_date[1][0]), int(res_date[1][1]), int(res_date[1][2])))
                            
                            new_task.lists_of_todolist.add(new_list)
        else:
            if todolist.objects.filter(name_of_task=data['name_of_task']).exists():
                #test_str += '7'
                duplicate = data['name_of_task']
                return Response({'error': f'List already has {duplicate} task'}, status=status.HTTP_400_BAD_REQUEST)
            
            if 'date' not in data or data['date'].lower() == 'now':
                new_task = todolist.objects.create(name_of_task=data['name_of_task'], done_or_not=False, date_field = datetime.now())
            else:
                res_date = dateParse(data)
                new_task = todolist.objects.create(name_of_task=data['name_of_task'], done_or_not=False, date_field = datetime(int(res_date[0][0]), int(res_date[0][1]), int(res_date[0][2]), int(res_date[1][0]), int(res_date[1][1]), int(res_date[1][2])))
        

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


@api_view(['POST'])
def test(request):
    data = request.data
    temp_date = data['date'].split('T')
    res_date = [temp_date[0].split('-')]
    res_date += [temp_date[1].split(':')]

    res_date2 = [int(res_date[0][0]), int(res_date[0][1]), int(res_date[0][2]), int(res_date[1][0]), int(res_date[1][1]), int(res_date[1][2])]

    return JsonResponse(res_date2, safe=False)
