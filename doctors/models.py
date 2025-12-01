from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15)
    image = models.ImageField(upload_to='doctors/', blank=True, null=True)

    def __str__(self):
        return self.name
