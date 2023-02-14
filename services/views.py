from django.db.models import F,Q
from django.core.exceptions import ObjectDoesNotExist

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from rest_framework import status
from rest_framework.decorators import action ,api_view
from rest_framework.response import Response
from rest_framework import permissions

from . import permissions as custom_permissions
from . import serializers
from . import models
from . pagination import DefaultPagination
from . filters import ServiceFilter


@api_view(['GET','PUT','HEAD'])
def my_location(request ):
    try:
        loc = models.Location.objects.get(user_id= request.user.id) 
    except ObjectDoesNotExist:
        return Response("Now you have to be  login first , in future it  will be taken from gps",status= status.HTTP_405_METHOD_NOT_ALLOWED)
    if request.method == 'GET':
        serializer = serializers.LocationSerialzer(loc)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = serializers.LocationSerialzer(loc, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

def range(x1,y1,x2,y2):
    x = (x2-x1)**2
    y = (y2-y1)**2
    res = x+y
    return res**(1/2)

class UstadViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.UstadSerialzer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ServiceFilter
    pagination_class = DefaultPagination
    permission_classes = [permissions.IsAuthenticated] # we need this permission only because currently we dont have live location of user
    search_fields = ['user__username']
    ordering_fields = ['rate_per_hour', 'avr_rating','user__username']
    
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return None
        my_loc = models.Location.objects.get(user_id = self.request.user.id)
        ustad_ids_in_range = models.Range.objects.filter(radius__gte = range(my_loc.x,my_loc.y,F('x'),F('y'))).values_list('ustad_id')
        return models.Ustad.objects.filter(user_id__in =ustad_ids_in_range)

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        (ustad,created)= models.Ustad.objects.get_or_create(pk=request.user.id)
        if request.method == 'GET':
            serializer = serializers.UstadSerialzer(ustad)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = serializers.UstadSerialzer(ustad, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
 
    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[permissions.IsAuthenticated])
    def my_range(self, request):
        try:
            ustad = models.Ustad.objects.get(pk=request.user.id)
        except ObjectDoesNotExist:
            return Response("you don't have this type of account",status= status.HTTP_403_FORBIDDEN)
        range = models.Range.objects.get(ustad_id=ustad.pk)

        if request.method == 'GET':
            serializer = serializers.RangeSerialzer(range)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = serializers.RangeSerialzer( range, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
 
    @action(detail= True )
    def userreviews(self,request,pk):
        order_ids = models.Order.objects.filter(ustad_id = pk,is_completed = True).values_list('pk')
        reviews = models.Review.objects.filter(pk__in = order_ids)   
        rate =0
        rate = [ review.rate for review in reviews] 
        print(sum(rate),reviews.count())
        rate = sum(rate) /reviews.count()   
        models.Ustad.objects.filter(pk = pk ).update(avr_rating = rate)
        serializer = serializers.ReviewSerializer(reviews,many = True)
        return Response(serializer.data)

    


class OrderViewSet(ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes =[custom_permissions.OrderPermission]

    def get_queryset(self):
        return models.Order.objects.filter(ustad_id = self.kwargs['ustad_pk'])

    def get_serializer_context(self):
        return {'ustad_id':self.kwargs['ustad_pk'],\
                "user_id":self.request.user.id if self.request.user.is_authenticated else None}

    @action(methods=['GET','PATCH'],detail=True,permission_classes = [custom_permissions.OrderUstadPermission])
    def accept_order(self,request,ustad_pk,pk):
        order = models.Order.objects.get(pk = pk)
        if request.method == 'GET':
            serializer = serializers.AcceptOrderSerializer(order)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            ustad_order = models.Order.objects.filter(Q(ustad_id = ustad_pk) & ~Q(pk = pk) & Q(is_accepted = True) &  Q(is_completed = False))
            print(ustad_order)
            if ustad_order :
                return Response ("you can't accept multiple order",status=status.HTTP_405_METHOD_NOT_ALLOWED)
            serializer = serializers.AcceptOrderSerializer(order,data = request.data)
            serializer.is_valid(raise_exception = True)
            serializer.save()
    
            set_ustad_status(ustad_pk)
            return Response(serializer.data)

    @action(methods=['GET','PATCH'],detail=True,permission_classes = [custom_permissions.OrderUserPermission])
    def complete_order(self,request,ustad_pk,pk):
        order = models.Order.objects.get(pk = pk)
        print(order)
        if request.method == 'GET':
            serializer = serializers.CompleteOrderSerializer(order)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            if not order.is_accepted:
                return Response("order is not accepted you cann't check complete ")
            serializer = serializers.CompleteOrderSerializer(order,data = request.data)
            serializer.is_valid(raise_exception = True)
            serializer.save()
            
            set_ustad_status(ustad_pk)

            return Response(serializer.data)

def set_ustad_status(ustad_pk):
    ustad_order = models.Order.objects.filter(ustad_id = ustad_pk,is_accepted = True , is_completed = False)
    if ustad_order:
        models.Ustad.objects.filter(pk = ustad_pk).update(status =False)
    else:
        models.Ustad.objects.filter(pk = ustad_pk).update(status =True)

class ReviewViewSet(ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = [custom_permissions.ReviewPermission]
    def create(self, request,order_pk, *args, **kwargs):
        order = models.Order.objects.get(pk = order_pk)
        if not order.is_completed:
            return Response('order is not completed. you can review only completed order.',status= status.HTTP_405_METHOD_NOT_ALLOWED)
      
        serializer = serializers.ReviewSerializer(data=request.data,context ={'user_id' :self.request.user.id,'order_id': order_pk} )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get_queryset(self):
        return models.Review.objects.filter(order_id=self.kwargs['order_pk'])


