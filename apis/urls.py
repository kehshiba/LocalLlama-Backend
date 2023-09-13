from django.contrib import admin
from django.urls import path

from .views import callprogram,chathistory,upload_audio

urlpatterns = [
    path('chat/<output>/', callprogram, name='callprogram'),
    path('chat/', chathistory, name='chathistory'),
    path('upload/', upload_audio, name='upload_audio'),

]