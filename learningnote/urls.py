from . import views
from django.urls import path,include
from django.conf.urls.static import static
from ProgramNote import settings


urlpatterns = [
    path('page/',views.page),
    path('edit/',views.edit)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

