from django.db import models

# name, description, location, employeeamount
class Company(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    location = models.CharField(max_length=100)
    employeeamount = models.IntegerField()

    class Meta:
        ordering=["created"]