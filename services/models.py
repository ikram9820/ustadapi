from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


User = get_user_model()

class Location(models.Model):
    x = models.FloatField(default=0.0)
    y = models.FloatField(default=0.0)
    user = models.OneToOneField(User, on_delete= models.CASCADE, related_name= 'location', primary_key= True)

    def __str__(self) -> str:
        return f'{self.user.username}\'s {self.x}, {self.y}'
        
    class Meta:
        ordering = ['user__username']


class Profession(models.Model):
    title = models.CharField(max_length=200)
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']

JOB_TYPE_CHOICES = [
        ('F','Fix Rate'),
        ('H','Hourly'),
        ('D','Daily'),
        ('M','Monthly')
    ]

class Ustad(models.Model):
    online = models.BooleanField(default=False)
    visibility_radius = models.DecimalField(max_digits=6,decimal_places=4,default=0)
    rate = models.DecimalField(max_digits=6,decimal_places=2,default=0)
    jop_type = models.CharField(max_length=1,choices=JOB_TYPE_CHOICES,default='H')
    description = models.TextField(default="")    
    user = models.ForeignKey(User,on_delete=models.CASCADE,primary_key=True)
    profession = models.ForeignKey(Profession, on_delete=models.PROTECT,related_name='ustad',default=1)

    class Meta:
        ordering = ['user__username']

    def __str__(self) -> str:
        return f'{self.ustad.user.username} range is {self.visibility_radius/1000} km'



class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('P','Pending'),
        ('R','Rejected'),
        ('A','Accepted'),
        ('S','Start'),
        ('C','Complete')
    ]
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(auto_now=True)
    rate = models.DecimalField(max_digits=6,decimal_places=2,default=0)
    jop_type = models.CharField(max_length=1,choices=JOB_TYPE_CHOICES,default='H')
    status = models.CharField(max_length=1,choices=ORDER_STATUS_CHOICES,default='P')
    user = models.ForeignKey(User, on_delete=models.PROTECT,related_name='order')
    ustad = models.ForeignKey(Ustad , on_delete= models.CASCADE, related_name='request')

    def __str__(self) -> str:
        return f'{self.user.username} order {self.ustad.user.username}'
    
    class Meta:
        ordering = ['start']

class Review(models.Model):
    rate = models.SmallIntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    review = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT,related_name='review_user')
    order = models.OneToOneField(Order , on_delete= models.CASCADE, related_name='order_review',primary_key=True)

