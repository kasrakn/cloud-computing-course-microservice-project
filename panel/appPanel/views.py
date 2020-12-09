from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.crypto import get_random_string, hashlib
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from . import models, utils
from .models import Guest, Restaurant, User, Food, Menu

import json

# Create your views here.


@csrf_exempt
def logout(request):
    if 'username' not in request.POST.keys():
        return JsonResponse({
            'status': 'Error',
            'message': 'user did not specified'
        }, encoder=DjangoJSONEncoder)
    
    user_obj = User.objects.get(username=request.POST['username'])
    user_obj.is_logedin = False
    user_obj.save()

    return JsonResponse({
        'status': 'OK',
        'message': 'user loged out'
    }, encoder=DjangoJSONEncoder)



@csrf_exempt
def enter(request):
    token = get_random_string(length=32)

    while User.objects.filter(token=token).count() != 0 and Guest.objects.filter(token=token).count() != 0:
        token = get_random_string(length=32)

    guest = Guest(token=token)
    guest.save()

    return JsonResponse({
        'status': 'OK',
        'message': f"""this user entered successfully as a guest - token: {token}"""
    }, encoder=DjangoJSONEncoder)



@csrf_exempt
def exit(request):
    if 'token' not in request.POST.keys():
        return JsonResponse({
        'status': 'Error',
        'message': 'guest not specified'
    }, encoder=DjangoJSONEncoder)
    
    token = request.POST['token']

    geust_obj = Guest.objects.get(token=token)
    geust_obj.delete()

    return JsonResponse({
        'status': 'OK',
        'message': 'guest successfully exited from the app'
    }, encoder=DjangoJSONEncoder)
