from django.urls import path
from . import views

urlpatterns = [
    path('formats/', views.formats, name='formats'),
]