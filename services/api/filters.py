from django_filters.rest_framework import FilterSet
from services.models import Gig

class GigFilter(FilterSet):
  class Meta:
    model = Gig
    fields = {
      'profession_id': ['exact'],
      'rate': ['gt', 'lt'],
      'is_active':['exact']
    }