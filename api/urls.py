from django.contrib import admin
from django.urls import path, include
from api.lanchonetes import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.lanchonetes.urls'))
]
