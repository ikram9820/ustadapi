from rest_framework import serializers
from services import models

class GigSerialzer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only = True)

    class Meta:
        model = models.Gig
        fields = ['user_id','user','rate','is_active','description','profession']

 
# class LocationSerialzer(serializers.ModelSerializer):
#     user_id = serializers.IntegerField(read_only = True)
    
#     class Meta:
#         model = models.Location
#         fields = ['user_id','x','y']


 
class OrderSerializer(serializers.ModelSerializer):
    ordered_at = serializers.DateTimeField(read_only = True)
    user_id = serializers.IntegerField(read_only = True)
    gig_id = serializers.IntegerField(read_only = True)
    class Meta:
        model = models.Order
        fields = ['id','gig_id','user_id','start_at','status']

    def create(self, validated_data):
        user_id = self.context['user_id']
        gig_id = self.context['gig_id']
        if not user_id:
            raise serializers.ValidationError("please login first!")
        (order,created) = models.Order.objects.get_or_create(user_id = user_id ,gig_id=gig_id,status="P",**validated_data)
        return order


class AcceptOrderSerializer(serializers.ModelSerializer):
    start = serializers.DateTimeField(read_only = True)
    user_id = serializers.IntegerField(read_only = True)
    gig_id = serializers.IntegerField(read_only = True)
    class Meta:
        model = models.Order
        fields = ['id','start_at','gig_id','user_id']


class CompleteOrderSerializer(serializers.ModelSerializer):
    start = serializers.DateTimeField(read_only = True)
    user_id = serializers.IntegerField(read_only = True)
    gig_id = serializers.IntegerField(read_only = True)
    class Meta:
        model = models.Order
        fields = ['id','start_at','gig_id','user_id']

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
