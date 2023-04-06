from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from rest_framework import permissions


class IsCreator(UserPassesTestMixin, View):
    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.creator
    
class IsSuperUser(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser


class IsCreatorOrSuperUserCheck(UserPassesTestMixin, View):
    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_superuser or self.request.user == obj.creator
    

class IsImplementorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.implementor == request.user