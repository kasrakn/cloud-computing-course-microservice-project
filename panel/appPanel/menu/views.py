from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from panel.appPanel.models import Menu, Restaurant
from panel.appPanel.utils import auth_checker



@csrf_exempt
def menu(request):
    if request.method == 'POST':
        if 'token' not in request.POST.keys():
            return JsonResponse({
                'status': 401,
                'message':'Unauthorised'
            }, encoder=DjangoJSONEncoder)

        if 'name' not in request.POST.keys():
            return JsonResponse({
                'status': 406,
                'message':'Not acceptable: there is no menu name'
            }, encoder=DjangoJSONEncoder)
        
        if 'username' not in request.POST.keys():
            return JsonResponse({
                'status': 401,
                'message':'Unauthorised'
            }, encoder=DjangoJSONEncoder)

        token = request.POST['token']
        username = request.POST['username']
        menu_name = request.POST['name']

        if auth_checker(username, token):
            rest_obj = Restaurant.objects.get(username=username)
            menu_obj = Menu(name=menu_name, username=username)
            menu_obj.save()

            return JsonResponse({
                'status': 200, 
                'message': 'OK'

            }, encoder=DjangoJSONEncoder)

        else:
            return JsonResponse({
                'status': 403,
                'message': 'Forbidden'

            }, encoder=DjangoJSONEncoder)
    

@csrf_exempt
def delete_menu(request):
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

        if Menu.objects.filter(username=username).count() != 0:
            menu_obj = Menu.objects.get(username=username)
            if auth_checker(menu_obj.username, token):
                    menu_obj.delete()
                    menu_obj.save()
            else:
                return JsonResponse({
                    'status': 403,
                    'message': 'Forbidden'
                }, encoder=DjangoJSONEncoder)