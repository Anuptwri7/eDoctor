from django.urls import path
from .views import view_doctors

urlpatterns = [
    path('doctors/', view_doctors, name='view_doctors'),
]
