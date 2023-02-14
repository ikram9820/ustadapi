from django_filters.rest_framework import FilterSet
from .models import Ustad

class ServiceFilter(FilterSet):
  class Meta:
    model = Ustad
    fields = {
      'category_id': ['exact'],
      'rate_per_hour': ['gt', 'lt'],
      'avr_rating': ['gt', 'lt'],
      'status':['exact']
    }