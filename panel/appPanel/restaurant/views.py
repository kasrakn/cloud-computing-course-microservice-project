from django.core.serializers.json import DjangoJSONEncoder
from django.core.signing import Signer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from panel.appPanel.models import Restaurant
from panel.appPanel.utils import auth_checker



@csrf_exempt
def get_restaurants(request):
    restaurants = Restaurant.objects.all()

    resp = {}

    for rest in restaurants:
        resp[f'{rest.user.username}'] = rest.username

    return JsonResponse(resp, encoder=DjangoJSONEncoder)


@csrf_exempt
def get_menu(request):
    if 'token' not in request.POST.keys():
        return JsonResponse({
        'status': 'Error',
        'message': 'restaurant has not been specified'
    }, encoder=DjangoJSONEncoder)

    token = request.POST['token']

    rest_obj = Restaurant.objects.get(token=token)
    menus = rest_obj.menus.all()
    
    menus_dic = {}

    for m in menus:
        foods = {}
        for f in m.foods.all():
            foods[f.name] = f.price
        menus_dic[f'{m.name}'] = foods

    return JsonResponse(menus_dic, encoder=DjangoJSONEncoder)



@csrf_exempt
def open_restaurant(request):
    if 'username' not in request.POST.keys():
        return JsonResponse({
            'status': 400,
            'message':'Bad Request'
        }, encoder=DjangoJSONEncoder)
    
    username = request.POST['username']

    if 'token' not in request.POST.keys():
        return JsonResponse({
            'status': 401,
            'message':'Unauthorized'
        }, encoder=DjangoJSONEncoder)
    
    token = request.POST['token']

    if Restaurant.objects.filter(username=username).count() != 0:
        rest_obj = Restaurant.objects.get(username=username)
        if auth_checker(rest_obj.username, token):
            rest_obj.is_open = True
            rest_obj.save()
        else:
            return JsonResponse({
                'status': 403,
                'message': 'Forbidden'
            }, encoder=DjangoJSONEncoder)

        return JsonResponse({
            'status': 200, 
            'message': 'OK'

        }, encoder=DjangoJSONEncoder)


@csrf_exempt
def close_restaurant(request):
    if 'username' not in request.POST.keys():
        return JsonResponse({
            'status': 400,
            'message':'Bad Request'
        }, encoder=DjangoJSONEncoder)
    
    username = request.POST['username']

    if 'token' not in request.POST.keys():
        return JsonResponse({
            'status': 401,
            'message':'Unauthorized'
        }, encoder=DjangoJSONEncoder)
    
    token = request.POST['token']

    if Restaurant.objects.filter(username=username).count() != 0:
        rest_obj = Restaurant.objects.get(username=username)
        if auth_checker(rest_obj.username, token):
            rest_obj.is_open = False
            rest_obj.save()
        else:
            return JsonResponse({
                'status': 403,
                'message': 'Forbidden'
            }, encoder=DjangoJSONEncoder)

        return JsonResponse({
            'status': 200, 
            'message': 'OK'

        }, encoder=DjangoJSONEncoder)


@csrf_exempt
def delete_restaurant(request):
    if request.method == 'POST':
        if 'username' not in request.POST.keys():
            return JsonResponse({
                'status': 400,
                'message':'Bad Request'
            }, encoder=DjangoJSONEncoder)

        if 'token' not in request.POST.keys():
            return JsonResponse({
                'status': 401,
                'message':'Unauthorized'
            }, encoder=DjangoJSONEncoder)
        
        username = request.POST['username']
        token = request.POST['token']

        if Restaurant.objects.filter(username=username).count() != 0:
            rest_obj = Restaurant.objects.get(username=username)
            if auth_checker(rest_obj.username, token):
                    rest_obj.delete()
                    rest_obj.save()
            else:
                return JsonResponse({
                    'status': 403,
                    'message': 'Forbidden'
                }, encoder=DjangoJSONEncoder)

@csrf_exempt
def restaurant_status(request):
    if 'username' not in request.POST.keys():
        return JsonResponse({
            'status': 'Error',
            'message':'restaurant token not specified'
        }, encoder=DjangoJSONEncoder)
    
    username = request.POST['username']

    if Restaurant.objects.filter(username=username).count() != 0:
        rest_obj = Restaurant.objects.get(username=username)

        if rest_obj.is_open:
            return JsonResponse({
                'status': 'OK', 
                'message': 'restaurant is open'

            }, encoder=DjangoJSONEncoder)
        else:
            return JsonResponse({
                'status': 'OK', 
                'message': 'restaurant is closed'

            }, encoder=DjangoJSONEncoder)
