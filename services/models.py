from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


ORDER_STATUS_PENDING='P'
ORDER_STATUS_CANCELLED='C'
ORDER_STATUS_REJECTED='R'
ORDER_STATUS_ACCEPTED='A'
ORDER_STATUS_FINISHED='F'

ORDER_STATUS_CHOICES = [
    (ORDER_STATUS_PENDING,'Pending'), #Ustads can have ONLY 3 ORDERS AT A TIME
    (ORDER_STATUS_CANCELLED,'Cancelled'), #Customer can cancel
    (ORDER_STATUS_REJECTED,'Rejected'), #Ustad can reject
    (ORDER_STATUS_ACCEPTED,'Accepted'), #Ustad can accept ONLY  ORDERS 3 AT A TIME
    (ORDER_STATUS_FINISHED,'Finished') #Agreement of both can complete
]

JOB_TYPE_FIX='F'
JOB_TYPE_HOURLY ='H'
JOB_TYPE_DAILY ='D'
JOB_TYPE_MONTHLY ='M'

JOB_TYPE_CHOICES = [
    (JOB_TYPE_FIX,'Fix Rate'),
    (JOB_TYPE_HOURLY,'Hourly'),
    (JOB_TYPE_DAILY,'Daily'),
    (JOB_TYPE_MONTHLY,'Monthly')
]

class Profession(models.Model):
    title = models.CharField(max_length=200)
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']


class Gig(models.Model):
    title = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False)
    visibility_radius = models.DecimalField(max_digits=6,decimal_places=4,default=0)
    rate = models.DecimalField(max_digits=6,decimal_places=2,default=0)
    jop_type = models.CharField(max_length=1,choices=JOB_TYPE_CHOICES,default=JOB_TYPE_FIX)
    description = models.TextField()   
    created_at = models.DateTimeField(auto_now_add=True) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    profession = models.ForeignKey(Profession, on_delete=models.PROTECT,related_name='gig',default=1)

    class Meta:
        ordering = ['user__username']

    def __str__(self) -> str:
        return f'{self.user.username} range is {self.visibility_radius/1000} km'




class Order(models.Model):
    start_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(auto_now=True)
    rate = models.DecimalField(max_digits=6,decimal_places=2,default=0)
    jop_type = models.CharField(max_length=1,choices=JOB_TYPE_CHOICES,default=JOB_TYPE_FIX)
    status = models.CharField(max_length=1,choices=ORDER_STATUS_CHOICES,default=ORDER_STATUS_PENDING)
    requirements = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,related_name='order')
    gig = models.ForeignKey(Gig , on_delete= models.CASCADE, related_name='request')

    def __str__(self) -> str:
        return f'{self.user.username} order {self.gig.user.username}'
    
    class Meta:
        ordering = ['start_at']

class Review(models.Model):
    rate = models.SmallIntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    review = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,related_name='review_user')
    order = models.OneToOneField(Order , on_delete= models.CASCADE, related_name='order_review',primary_key=True)

