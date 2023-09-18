from django.contrib import admin
from django.urls import path

from .views import callprogram,abort_code,upload_audio,save_log

urlpatterns = [
    path('chat/<str:output>/', callprogram, name='callprogram'),
    path('chat/save', save_log, name='savelog'),
    path('upload/', upload_audio, name='upload_audio'),
    path('abort/', abort_code, name='abort_code'),

]