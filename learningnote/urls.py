from . import views
from django.urls import path,include
from django.conf.urls.static import static
from ProgramNote import settings


urlpatterns = [
    path('page/',views.page),
    path('authPage/', views.authPage),

    path('edit/',views.edit),
    path('editTheme/',views.editTheme),

    path('createTheme/',views.createTheme),
    path('createSubTheme/',views.createSubTheme),
    path('createNote/',views.createNote),

    path('deleteNote/',views.deleteNote),

    path('auth/',views.auth)

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

