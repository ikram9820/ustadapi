from cgitb import lookup
from email.mime import base
from rest_framework_nested import routers
from django.urls import path
from . import views


router = routers.DefaultRouter()

router.register('gigs', views.GigViewSet, basename='gigs')
gigs_router = routers.NestedDefaultRouter(router,'gigs',lookup = 'gig')
gigs_router.register('orders',views.OrderViewSet,basename='service-orders')
order_router = routers.NestedDefaultRouter(gigs_router,'orders',lookup = 'order')
order_router.register('reviews',views.ReviewViewSet,basename='oreder-review')

urlpatterns = router.urls + gigs_router.urls +order_router.urls 