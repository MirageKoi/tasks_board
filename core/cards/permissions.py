from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin


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