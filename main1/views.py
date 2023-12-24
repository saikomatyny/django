import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

def get_endpoint(request):
    data = {'message': 'TEST'}
    return JsonResponse(data)

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
    return render(request, 'main1/index.html')
