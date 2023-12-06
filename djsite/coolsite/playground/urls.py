from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('', views.index, name='homepage'),
    path('process_form/', views.process_form, name='process_form'),
]
