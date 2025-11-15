from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf.urls.static import static

from medi_guide import settings


def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('home')
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_redirect, name='root_redirect'),
    path('', include('users.urls')),
    path('checkup/', include('checkup.urls')),
    path('', include('doctors.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
