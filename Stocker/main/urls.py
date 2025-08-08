from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('signup/', views.signup_view, name='signup_view'),   
    path('login/', views.login_view, name='login_view'),     
    path('logout/', views.logout_view, name='logout_view'),  
    path('dashboard/', views.dashboard_view, name='dashboard_view'), 
]
