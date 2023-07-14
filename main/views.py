import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
import json
import os
from django.contrib.auth.decorators import login_required
from .models import Theme,User,Contact,Auth

def main(request):
    if request.method == 'POST':
        if request.user.is_authenticated == False:
            return HttpResponse()
        themes= Theme.objects.filter(author_id = request.user).all().values("title")
        auth = Auth.objects.filter(authUser = request.user).all()
        auth = list(map(lambda a:{'title':a.authTheme.title,'id':a.authTheme.id},auth))
        print(auth)
        return JsonResponse({'data':list(themes),'authData':auth})
    else:
        return render(request, 'index.html')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        username = req['username']
        password = req['password']
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return JsonResponse({'errno': 0})
        return JsonResponse({'errno': 1})

def uniqueUser(request):
    req = json.loads(request.body)
    username = req['username']
    user = User.objects.filter(username = username).first()
    if user != None:
        print('重複')
        return JsonResponse({"isUnique":False})
    else:
        return JsonResponse({'isUnique':True})

def register(request):
    if request.method == 'POST':
        try:
            req = json.loads(request.body)
            username = req['username']
            password = req['password']
            User.objects.create_user(username = username,password = password)
            return JsonResponse({'errno': 1})
        except:
            return JsonResponse({'errno': 2})


def handler404(request, exception):
    return render(request, 'error/404.html', status=404)




