
from django.contrib import admin
from django.urls import path,include

from apis import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include("apis.urls")),
    path('get-csrf-token/', views.get_csrf_token, name='get_csrf_token'),

]
