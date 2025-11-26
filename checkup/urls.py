from django.urls import path
from . import views
from .views import start_checkup_view, recheck_checkup_view
from doctors.views import doctor_detail_view

urlpatterns = [
    path('start/', start_checkup_view, name='start_checkup'),
    path('doctor/<int:pk>/', doctor_detail_view, name='doctor_detail'),
    path('checkup/<int:pk>/recheck/', recheck_checkup_view, name='recheck_checkup'),
    ]
