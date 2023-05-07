import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
import json
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from main.models import Theme,Note,Sub_Theme



@csrf_exempt
def page(request):
    theme = request.GET.get('theme', None)
    page = request.GET.get('page',1)
    ok_theme = Theme.objects.filter(note_title=theme).first()
    if ok_theme == None:
        return render(request, 'error/404.html')
    if request.method == 'GET':
        split_theme = str(ok_theme.note_title).replace(' ','')
        return render(request, 'note.html', locals())
    if request.method == 'POST':
        notes = ok_theme.note.all()
        list = []
        titles = []
        for note in notes:
            data = {}
            title = {}
            # main_title 第二等級的標題
            data['id'] = note.id
            data['main_title'] = note.sub_theme.sub_title
            data['title'] = note.title
            data['text'] = note.text
            if note.picture:
                data['picture'] = str(note.picture)
            else:
                data['picture'] = None
            data['code'] = note.code

            # 側邊欄加載
            # title['main_title'] = note.theme.note_title
            title['main_title'] = note.sub_theme.sub_title
            title['sub_title'] = note.title
            list.append(data)
            titles.append(title)
        return JsonResponse({'data':list,'titles':titles})


@login_required
@csrf_exempt
def edit(request):
    if request.user.is_superuser:
        title = request.GET.get('sub_theme', None)
        note_obj = Note.objects.filter(title=title).first()
        theme = note_obj.sub_theme.main_title.note_title
        if request.method == 'GET':
            return render(request,'edit.html',locals())
        if request.method == 'POST':
            req = json.loads(request.body)
            title = req['title']
            text = req['text']
            code = req['code']
            note_obj.title = title
            note_obj.save()
            return JsonResponse({'errno':0})
    else:
        return render(request, 'error/403.html')




