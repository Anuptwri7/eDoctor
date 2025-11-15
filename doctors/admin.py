from django.contrib import admin
from .models import Department, Doctor

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'contact_number', 'image')  # show image column
    list_filter = ('department',)
    search_fields = ('name',)
