from rest_framework import serializers
from companyservice.quickstart.models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'description', 'employeeamount', 'location', 'created']