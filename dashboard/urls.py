from django.urls import path
from . import views
from usuarios import views


urlpatterns = [
    # ... outras URLs do seu projeto ...
    path('', views.login_usuario, name='login'),
    path('', views.home, name='home'),
    
   
    
    
    
]