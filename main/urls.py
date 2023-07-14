from . import views
from django.urls import path,include
from django.conf.urls.static import static
from ProgramNote import settings


urlpatterns = [
    path('',views.main),
    path('isUnique/',views.uniqueUser),
    path('login/api/',views.login),
    path('register/api/',views.register),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


