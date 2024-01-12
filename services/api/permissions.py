from rest_framework import permissions
from services import models
from django.core.exceptions import ObjectDoesNotExist

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)

    

class OrderPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )

        
    def has_object_permission(self, request, view, obj):
        
        if self.has_permission(request,view):
            return bool(obj.gig_id == request.user.id) or bool(obj.user_id == request.user.id) #tested just for order
        return False

class ReviewPermission(permissions.BasePermission):
    def has_permission(self, request,view):
        order_pk = view.kwargs['order_pk']
        if bool(
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        ):
            try:
                models.Order.objects.get(pk = order_pk , user_id =request.user.id)
                return True
            except ObjectDoesNotExist:
                return False
        return False

        
    def has_object_permission(self, request, view, obj):
        
        if self.has_permission(request,view):
            return bool(obj.user.id == request.user.id)  
        return False




class OrderUserPermission(permissions.BasePermission):
        
    def has_object_permission(self, request, view, obj):
        if bool(request.user and request.user.is_authenticated):
            return bool(obj.user_id == request.user.id) #tested just for order
        return False

class OrderGigPermission(permissions.BasePermission):

        
    def has_object_permission(self, request, view, obj):
        if bool(request.user and request.user.is_authenticated):
            return bool(obj.gig_id == request.user.id) #tested just for order
        return False

