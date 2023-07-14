from django.contrib import admin
from main.models import Note,Theme,SubTheme,User,Contact,Auth

admin.site.register(User)
admin.site.register(Note)
admin.site.register(Theme)
admin.site.register(SubTheme)
admin.site.register(Contact)
admin.site.register(Auth)


