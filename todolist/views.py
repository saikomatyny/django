import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import todolists

def get_endpoint(request):
    todolist_objects = todolists.objects.all()
    '''todolist_values_dict = {}

    for obj in todolist_objects:
        todolist_values_dict[obj.name_of_task] = obj.done_or_not

    return JsonResponse(todolist_values_dict)'''
    todolist_values_list = list(todolist_objects.values())

    return JsonResponse(todolist_values_list, safe=False)

@csrf_exempt
def post_endpoint(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            
            response_data = {'status': 'success', 'message': 'Данные успешно получены'}
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            response_data = {'status': 'error', 'message': 'Ошибка в формате JSON'}
            return JsonResponse(response_data, status=400)
    else:
        response_data = {'status': 'error', 'message': f'Метод не разрешен {request}'}
        return JsonResponse(response_data, status=405)


def index(request):
    data = {
        'title': 'example #1',
        'main_text' : 'test test test',
        'list' : [1, 2, 3, '4', '5']
    }
    return render(request, 'main1/index.html', data)
