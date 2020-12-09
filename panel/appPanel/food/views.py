from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from panel.appPanel.models import Restaurant,Menu, Food

@csrf_exempt
def add_food(request):
    if 'name' not in request.POST.keys():
        return JsonResponse({
            'status': 'Error',
            'message': 'food name field is empty'
        }, encoder=DjangoJSONEncoder)

    if 'price' not in request.POST.keys():
        return JsonResponse({
            'status': 'Error',
            'message': 'food price field is empty'
        }, encoder=DjangoJSONEncoder)

    if 'availablity' in request.POST.keys():
        availablity = int(request.POST["availablity"])

    name  = request.POST['name']
    price = request.POST['price']

    food_obj = Food(name=name, price=price, availablity=availablity)
    food_obj.save()

    return JsonResponse({
        'status': 'OK', 
        'message': 'Food successfully added'
    }, encoder=DjangoJSONEncoder)

    


@csrf_exempt
def add_to_menu(request):
    if 'token' not in request.POST.keys():
        return JsonResponse({
            'status': 'Error',
            'message': 'restaurant tokon not specified'
        }, encoder=DjangoJSONEncoder)        

    if 'menu_id' not in request.POST.keys():
        return JsonResponse({
            'status': 'Error',
            'message': 'menu id not specified'
        }, encoder=DjangoJSONEncoder)
    
    if 'food_id' not in request.POST.keys():
        return JsonResponse({
            'status': 'Error',
            'message': 'food id not specified'
        }, encoder=DjangoJSONEncoder)

    rest_token = request.POST['token']
    menu_id = request.POST['menu_id']
    food_id = request.POST['food_id']

    if Restaurant.objects.filter(token=rest_token).count() != 0:
        rest_obj = Restaurant.objects.get(token=rest_token)
        menu_obj = Menu.objects.get(id=menu_id)
        food_obj = Food.objects.get(foodID=food_id)
        menu_obj.foods.add(food_obj)
        menu_obj.save()

        return JsonResponse({
            'status': 'OK', 
            'message': 'food added successfuly to the menu'
        }, encoder=DjangoJSONEncoder)
        
    