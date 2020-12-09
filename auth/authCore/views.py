from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.serializers.json import DjangoJSONEncoder
from django.core.signing import Signer
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt

from .models import User
# from .permissions import IsOwnerOrReadOnly
from .serializers import UserLoginSerializer, UserSerializer


@csrf_exempt
def user(request):
    """register a user in system"""

    if request.method == 'POST':

        if 'username' not in request.POST.keys():
            
            # user with no username is an Anonimous user
            new_user = AnonymousUser()
        else:
            this_username = request.POST['username']
            
            if 'email' in request.POST.keys():
                email = request.POST['email']
            else:
                return JsonResponse({
                    'status' : 400,
                    'message': 'BAD_REQUEST : email is not passed'
                }, encoder=DjangoJSONEncoder)

            if 'password' in request.POST.keys():
                password = request.POST['password']
            else:
                return JsonResponse({
                    'status': 400,
                    'message': 'BAD REQUEST: password was not passed with request'
                })

            # define what type is the user
            if 'role' in request.POST.keys():

                is_restaurant = True if int(request.POST['role']) == 1 else False
            else:
                return JsonResponse({
                    'status': 400,
                    'message': 'BAD_REQUEST : role is empty'
                }, encoder=DjangoJSONEncoder)

            # Duplicate username error: another user already has chosen this username 
            if User.objects.filter(username=this_username).count() != 0:
                return JsonResponse({
                    'status': 406,
                    'message:' :'METHOD NOT ALLOWED: another user with this username is available'
                }, encoder=DjangoJSONEncoder)

            new_user = User(username=this_username, 
                            email=email, 
                            password=password, 
                            date_joined=datetime.now(), 
                            is_staff=is_restaurant, 
                            last_login=datetime.now(),
                            is_superuser=False
                            )
        new_user.save()
        return JsonResponse({
            'status' : 200,
            'message' : 'OK'
        }, encoder=DjangoJSONEncoder)

    elif request.method == 'GET':
        users = User.objects.all()
        repr_users =  {f'{v}' : repr(i) for i, v in enumerate(users)}

        return JsonResponse({
            'status': 200,
            'message': 'users list fetched'
        }, encoder=DjangoJSONEncoder)


@csrf_exempt
def user_detail(request, pk):
    if request.method == "GET":
        user = User.objects.get(pk=pk)[0]

        return JsonResponse({
            "data" : repr(user),
            "status": 200,
            "message":"user fetched"
        }, encoder=DjangoJSONEncoder)
    else:
        return JsonResponse({
            'status': 400,
            'message': 'BAD REQUEST'
        }, encoder=DjangoJSONEncoder)


@csrf_exempt
def login(self, request):
    if 'username' not in request.POST.keys():
        return JsonResponse({
            'status': 400,
            'message': 'BAD REQUEST : no username in request'
        }, encoder=DjangoJSONEncoder)
    else:
        this_username = request.POST['username']
        
        if 'password' in request.POST.keys():
            email = request.POST['password']
        else:
            return JsonResponse({
                'status': 400,
                'message': 'BAD REQUEST : no password in request'
            }, encoder=DjangoJSONEncoder)

        obj = get_user_model().objects.get(username=this_username)
        if this_username == obj.password:
            return JsonResponse({
                'status': 200,
                'message': 'OK',
            }, encoder=DjangoJSONEncoder)


@csrf_exempt
def authentication_checker(request):
    if request.method == 'POST':
        
        if 'username' not in request.POST.keys() or 'token' not in request.POST.keys():
            return JsonResponse({
                'status': 406,
                'message': 'Not Acceptable'
            }, encoder=DjangoJSONEncoder)
        
        username = request.POST['username']
        token = request.POST['token']

        user_obj = User.objects.get(username=username)

        signer = Signer()
        if signer.sign(str(user_obj.username) + str(user_obj.password)) != token:
            return DjangoJSONEncoder({
                'status': 403,
                'message': 'Forbidden'
            }, encoder=DjangoJSONEncoder)
        
        return JsonResponse({

            'status': 200,
            'message': 'OK'
        }, encoder=DjangoJSONEncoder)

