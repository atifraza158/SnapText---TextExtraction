from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . views import *


urlpatterns = [
    path('', home, name='home'),
    path('text_extraction', text_extraction, name='text-extraction'),
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)