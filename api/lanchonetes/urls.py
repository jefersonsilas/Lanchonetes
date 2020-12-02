from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('api/autenticacao/', views.Login.as_view()),
    path('api/autenticacao/0', views.Logout.as_view()),
    path('api/lojas/', views.LojasList.as_view()),
    path('api/lojas/<int:pk>/', views.LojaDetail.as_view()),
    path('api/produtos/', views.ProdutosList.as_view()),
    path('api/produtos/<int:pk>/', views.ProdutoDetail.as_view()),
    path('api/promocoes/', views.PromocoesList.as_view()),
    path('api/promocoes/<int:pk>/', views.PromocaoDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)