# doctors/views.py
from django.shortcuts import render
from .models import Doctor
from django.shortcuts import render, get_object_or_404
from .models import Doctor

def view_doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctors/view_doctors.html', {'doctors': doctors})


def doctor_detail_view(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    return render(request, 'doctors/doctor_detail.html', {'doctor': doctor})
