from django_filters.rest_framework import FilterSet
from .models import Ustad

class ServiceFilter(FilterSet):
  class Meta:
    model = Ustad
    fields = {
      'profession_id': ['exact'],
      'rate': ['gt', 'lt'],
      'online':['exact']
    }