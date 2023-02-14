from cgitb import lookup
from email.mime import base
from rest_framework_nested import routers
from django.urls import path
from . import views


router = routers.DefaultRouter()

router.register('ustads', views.UstadViewSet, basename='ustads')
ustads_router = routers.NestedDefaultRouter(router,'ustads',lookup = 'ustad')
ustads_router.register('orders',views.OrderViewSet,basename='service-orders')
order_router = routers.NestedDefaultRouter(ustads_router,'orders',lookup = 'order')
order_router.register('reviews',views.ReviewViewSet,basename='oreder-review')

urlpatterns =[
path('my_location/',views.my_location),
] + router.urls + ustads_router.urls +order_router.urls 