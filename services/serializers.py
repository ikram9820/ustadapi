from rest_framework import serializers
from django.db.models import Q 
from django.core.exceptions import ObjectDoesNotExist
from . import models

class UstadSerialzer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only = True)

    class Meta:
        model = models.Ustad
        fields = ['user_id','user','rate_per_hour','status','description','category']

 
class LocationSerialzer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only = True)
    
    class Meta:
        model = models.Location
        fields = ['user_id','x','y']

class RangeSerialzer(serializers.ModelSerializer):
    
    ustad_id = serializers.IntegerField(read_only = True)
    ustad = serializers.StringRelatedField(read_only =True)
    class Meta:
        model = models.Range
        fields = ['ustad','ustad_id','x','y','radius','address']

 
class OrderSerializer(serializers.ModelSerializer):
    ordered_at = serializers.DateTimeField(read_only = True)
    user_id = serializers.IntegerField(read_only = True)
    ustad_id = serializers.IntegerField(read_only = True)
    is_accepted = serializers.BooleanField(read_only = True)
    is_completed = serializers.BooleanField(read_only = True)
    class Meta:
        model = models.Order
        fields = ['id','ordered_at','ustad_id','user_id','is_accepted','is_completed']

    def create(self, validated_data):
        user_id = self.context['user_id']
        ustad_id = self.context['ustad_id']
        if not user_id:
            raise serializers.ValidationError("please login first!")
        (order,created) = models.Order.objects.get_or_create(user_id = user_id ,ustad_id=ustad_id,is_completed = False,**validated_data)
        return order


class AcceptOrderSerializer(serializers.ModelSerializer):
    ordered_at = serializers.DateTimeField(read_only = True)
    user_id = serializers.IntegerField(read_only = True)
    ustad_id = serializers.IntegerField(read_only = True)
    is_completed = serializers.BooleanField(read_only = True)
    class Meta:
        model = models.Order
        fields = ['id','ordered_at','ustad_id','user_id','is_accepted','is_completed']


class CompleteOrderSerializer(serializers.ModelSerializer):
    ordered_at = serializers.DateTimeField(read_only = True)
    user_id = serializers.IntegerField(read_only = True)
    ustad_id = serializers.IntegerField(read_only = True)
    is_accepted = serializers.BooleanField(read_only = True)
    class Meta:
        model = models.Order
        fields = ['id','ordered_at','ustad_id','user_id','is_accepted','is_completed']

class ReviewSerializer(serializers.ModelSerializer):

    order_id = serializers.IntegerField(read_only= True)
    user_id = serializers.IntegerField(read_only= True)

    class Meta:
        model = models.Review
        fields = ['rate', 'review', 'user_id','order_id']

    def create(self, validated_data):
        order_id = self.context['order_id']
        user_id = self.context['user_id']
        (review,created) = models.Review.objects.get_or_create(pk = order_id, user_id= user_id)
        review.rate =validated_data['rate']
        review.review = validated_data['review']
        review.save()
        return review
