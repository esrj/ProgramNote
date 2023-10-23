from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from main.models import Theme,Note,SubTheme,User


@login_required
@csrf_exempt
def page(request):
    createTheme = False
    # 沒有query string 時 前往新增頁面
    if request.GET.get('theme', None) == None:
        createTheme = True
        return render(request, 'note.html', locals())
    theme = Theme.objects.filter(title=request.GET.get('theme'),author_id = request.user).first()
    # 主題不存在
    if theme == None:
        return render(request,'error/404.html')
    # 加載主題中的 標題
    sub = request.GET.get('page', None)
    subThemeObj = theme.sub.first()
    if sub != None:
        okSubThemeObj = SubTheme.objects.filter(title=sub,theme = theme).first()
        if okSubThemeObj != None:
            subThemeObj = okSubThemeObj
    # 如果 query string 有指定 標題就加在該標題，若沒有，就加在第一個。如果整個主題是空的 subThemeObj = None

    if request.method == 'GET':
        return render(request, 'note.html', locals())
    # 筆記頁面 非同步載入
    if request.method == 'POST':
        sideBar=[{'mainTitle':theme.title}]
        # 側邊欄加載
        if subThemeObj != None:
            # 擁有標題
            subThemes = theme.sub.all()
            for subTheme in subThemes:
                sideBar.append({'subTitle':subTheme.title})
                notes = subTheme.note.all()
                for note in notes:
                    sideBar.append({'noteTitle':note.title,'subTitle':subTheme.title,'id':note.id})
            # 筆記加載
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

def createTheme(request):
    req = json.loads(request.body)
    title = req['title']
    introduce = req['introduce']
    if title.replace(' ','').replace('\n','') == '':
        return JsonResponse({'errno': 1})
    else:
        Theme.objects.create(title = title,introduce = introduce,author_id = request.user).save()
        return JsonResponse({'errno':0})

def createSubTheme(request):
    req = json.loads(request.body)
    subTheme = req['subTheme']
    if subTheme.replace(' ','') == '':
        return JsonResponse({'errno': 2})
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
    if request.method == 'POST':
        req = json.loads(request.body)

        title = req['title'].replace('\n','')
        if title.replace(' ','') == '':
            return JsonResponse({'errno':2})
        text = req['text']
        code = req['code']
        theme = Theme.objects.filter(title = theme,author_id = request.user).first()
        if theme:
            subtheme =SubTheme.objects.filter(theme = theme).first()
            if subtheme == None:
                newSubtheme = SubTheme.objects.create(title = title,theme = theme)
                newSubtheme.save()
                note = Note.objects.create(title=title, text=text, code=code, theme=theme, subTheme=newSubtheme)
                note.save()
            else:
                if sub == None or sub == 'None':
                    print(subtheme)
                    note = Note.objects.create(title=title, text=text, code=code, theme=theme, subTheme=subtheme)
                    note.save()
                else:
                    subtheme = SubTheme.objects.filter(title = sub,theme = theme).first()
                    note = Note.objects.create(title=title, text=text, code=code, theme=theme, subTheme=subtheme)
                    note.save()
            return HttpResponse()


@login_required
def edit(request):
    if request.method == "POST":
        req = json.loads(request.body)
        theme = Theme.objects.filter(title = req['theme'],author_id = request.user).first()
        if theme:
            note = Note.objects.filter(id=int(req['id'])).first()
            if note:
                if req['action'] == 'edit':
                    title = req['title'].replace('\n', '')
                    if title.replace(' ','').replace('\n','') == '':
                        return JsonResponse({'errno': 1})

                    text = req['text']
                    code = req['code']
                    note.title = title
                    note.text = text
                    note.code = code
                    note.save()
                    return JsonResponse({'errno': 0})
                elif  req['action'] == 'delete':
                    note.delete()
                    return JsonResponse({'errno': 0})
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
