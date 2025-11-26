from django.urls import path
from . import views
from django.urls import path
from checkup import views as checkup_views
urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('contact/', views.contact_view, name='contact'),
    path("checkups/", checkup_views.checkup_list_view, name="checkup_list"),
    path("checkups/<int:pk>/", checkup_views.checkup_detail_view, name="checkup_detail"),
]

