from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from main.models import Theme,Note,SubTheme,Auth,User


@login_required
@csrf_exempt
def page(request):
    if request.GET.get('theme', None) == None:
        return render(request, 'createTheme.html')
    theme = Theme.objects.filter(title=request.GET.get('theme'),author_id = request.user).first()
    if theme == None:
        return render(request,'error/404.html')
    sub = request.GET.get('page', None)
    subThemeObj = theme.sub.first()
    if sub != None:
        okSubThemeObj = SubTheme.objects.filter(title=sub,theme = theme).first()
        if okSubThemeObj != None:
            subThemeObj = okSubThemeObj
    if request.method == 'GET':
        return render(request, 'note.html', locals())
    if request.method == 'POST':
        sideBar=[{'mainTitle':theme.title}]
        # 側邊欄加載
        if subThemeObj != None:
            subThemes = theme.sub.all()
            for subTheme in subThemes:
                sideBar.append({'subTitle':subTheme.title})
                notes = subTheme.note.all()
                for note in notes:
                    sideBar.append({'noteTitle':note.title})
            # 筆記家載
            notes = []
            for note in subThemeObj.note.all():
                data={}
                data['title'] = note.title
                data['text'] = note.text
                data['picture'] = None
                data['code'] = note.code
                data['id'] = note.id
                notes.append(data)
            return JsonResponse({'sideBar': sideBar,  'notes': notes})
        else:
            return JsonResponse({'sideBar':sideBar,'subTheme':'尚未建立章節','notes':[]})

@login_required
def authPage(request):
    theme = Theme.objects.filter(id=request.GET.get('theme')).first()
    if theme != None:
        auth = Auth.objects.filter(authTheme = theme,authUser = request.user).first()
        if auth != None :
            # 已經確認是有加載權限的
            # 是否有指定副標題
            sub = request.GET.get('page', None)
            subThemeObj = theme.sub.first()
            if sub != None:
                okSubThemeObj = SubTheme.objects.filter(title=sub, theme=theme).first()
                if okSubThemeObj != None:
                    subThemeObj = okSubThemeObj
            if request.method == 'GET':
                return render(request, 'authNote.html', locals())
            elif request.method =='POST':
                # 側邊欄加載
                sideBar = [{'mainTitle': theme.title}]
                subThemes = theme.sub.all()
                for subTheme in subThemes:
                    sideBar.append({'subTitle': subTheme.title})
                    notes = subTheme.note.all()
                    for note in notes:
                        sideBar.append({'noteTitle': note.title})
                 # 筆記家載
                notes = []
                for note in subThemeObj.note.all():
                    data = {}
                    data['title'] = note.title
                    data['text'] = note.text
                    data['picture'] = None
                    data['code'] = note.code
                    data['id'] = note.id
                    notes.append(data)
                return JsonResponse({'sideBar': sideBar, 'subTheme': subThemeObj.title, 'notes': notes})


    return render(request, 'error/404.html')

def createTheme(request):
    req = json.loads(request.body)
    title = req['title']
    introduce = req['introduce']
    theme = Theme.objects.create(title = title,introduce = introduce,author_id = request.user)
    theme.save()
    return JsonResponse({'errno':0})

def createSubTheme(request):
    req = json.loads(request.body)
    subTheme = req['subTheme']
    id = req['theme_id']
    theme = Theme.objects.filter(id = id,author_id =request.user).first()
    if SubTheme.objects.filter(theme = theme ,title = subTheme).first():
        return JsonResponse({'errno':1})
    sub_theme = SubTheme.objects.create(title = subTheme,theme = theme)
    sub_theme.save()
    return JsonResponse({'errno':0})

def createNote(request):
    sub = request.GET.get('page',None)
    theme = request.GET.get('theme')
    if request.method == 'GET':
        return render(request,'edit.html',locals())
    if request.method == 'POST':
        req = json.loads(request.body)
        title = req['title']
        text = req['text']
        code = req['code']
        theme = Theme.objects.filter(title = theme,author_id = request.user).first()
        if theme:
            subtheme =SubTheme.objects.filter(theme = theme).first()
            if subtheme == None:
                return JsonResponse({'errno':1})
            if sub != None:
                subtheme = SubTheme.objects.filter(title = sub,theme = theme).first()
            note = Note.objects.create(title = title,text = text,code = code,theme = theme,subTheme = subtheme)
            note.save()
        return HttpResponse()


def deleteNote(request):
    req = json.loads(request.body)
    theme = req['theme']
    subTheme = req['subTheme']
    noteTitle = req['noteTitle']
    try:
        theme = Theme.objects.filter(title=theme, author_id=request.user).first()
        subTheme = SubTheme.objects.filter(theme=theme,title = subTheme ).first()
        note = Note.objects.filter(subTheme = subTheme,theme = theme, title = noteTitle).first()
        note.delete()
    except:
        return render(request, 'error/403.html')
    return HttpResponse()

@login_required
def edit(request):
    theme = Theme.objects.filter(title = request.GET.get('theme'),author_id=request.user).first()
    if theme:
        subTheme = SubTheme.objects.filter(theme = theme ,title = request.GET.get('page')).first()
        if subTheme:
            id = request.GET.get('id', None)
            try:
                int(id)
            except:
                return render(request, 'error/403.html')
            note_obj = Note.objects.filter(theme = theme,subTheme = subTheme,id=int(id)).first()
            if note_obj:
                theme = note_obj.subTheme.theme.title
                if request.method == 'GET':
                    edit = True
                    return render(request,'edit.html',locals())
                if request.method == 'POST':
                    req = json.loads(request.body)
                    title = req['title']
                    text = req['text']
                    code = req['code']
                    note_obj.title = title
                    note_obj.text = text
                    note_obj.code = code
                    note_obj.save()
                    return JsonResponse({'errno':0})
    return render(request, 'error/403.html')


def editTheme(request):
    id = request.GET.get('id',None)
    try:
        int(id)
    except:
        return render(request, 'error/403.html')
    theme = Theme.objects.filter(id = int(id),author_id = request.user).first()
    if theme:
        if request.method == 'GET':
            subtheme = theme.sub.all()
            subtheme = list(map(lambda s:{'title':s.title,'id':s.id},subtheme))
            return render(request,'editTheme.html',locals())
        elif request.method == 'POST':
            req = json.loads(request.body)
            if req['index'] == 1:
                title = req['title']
                introduce = req['introduce']
                theme.title = title
                theme.introduce = introduce
                theme.save()
            if req['index'] == 2:
                theme.delete()
            if req['index'] == 3:
                id = req['id']
                title = req['title']
                subtheme = SubTheme.objects.filter(id = id).first()
                subtheme.title = title
                subtheme.save()
            if req['index'] ==4:
                id = req['id']
                subtheme = SubTheme.objects.filter(id=id).first()
                subtheme.delete()
            return JsonResponse({'errno':0})
    return render(request, 'error/403.html')
@login_required
def auth(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        try:
            if req['index'] == 1:
                username = req['username']
                users = User.objects.filter(username__contains = username).all()
                users = list(map(lambda u:{'id':u.id,"username":u.username},users))

                theme = Theme.objects.filter(id = req['theme_id']).first()
                allAuth = Auth.objects.filter(authTheme = theme).all()
                allAuth = list(map(lambda a:a.authUser.username, allAuth))
                for user in users:
                    if int(user['id']) == int(request.user.id):
                        users.remove(user)
                for user in users:
                    if user['username'] in allAuth:
                        users.remove(user)
                return JsonResponse({'users':users})
            elif req['index'] == 2:
                theme = Theme.objects.filter(id = req['theme_id'],author_id = request.user).first()
                if theme:
                    user = User.objects.filter(id = int(req['user_id'])).first()

                    auth = Auth.objects.create(authTheme = theme ,authUser = user )
                    auth.save()
                    return JsonResponse({'errno': 0})
            elif req['index'] == 3:
                theme = Theme.objects.filter(id = req['theme_id']).first()
                auths = Auth.objects.filter(authTheme = theme).all()
                auths = list(map(lambda a:a.authUser.username,list(auths)))
                return JsonResponse({'auths':auths})
            elif req['index'] == 4:
                username = req['username']
                user = User.objects.filter(username = username).first()
                theme = Theme.objects.filter(id = req['theme_id'],author_id = request.user).first()
                auth = Auth.objects.filter(authUser = user,authTheme = theme).first()
                auth.delete()
                return JsonResponse({'errno': 0})
        except:
            return JsonResponse({'errno': 1})
        return HttpResponse
    if request.method == "GET":
        return render(request, 'error/403.html')




'''

'''
