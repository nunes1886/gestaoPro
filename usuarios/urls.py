from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('deletar-item/<str:tipo>/<int:item_id>/', views.deletar_item, name='deletar_item'),
]