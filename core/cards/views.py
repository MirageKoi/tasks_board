from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from django.views.generic.edit import BaseUpdateView, FormView, ProcessFormView, FormMixin

from .forms import  CardCreateForm, HelperCardStatusUpdate, CardStatusUpdate, CardUpdateForm
from .models import CardModel
from .permissions import IsCreatorOrSuperUserCheck, IsSuperUser, IsCreator

from django.contrib.auth.mixins import UserPassesTestMixin

from rest_framework import generics
from .serializers import CardSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated



class CardListView(ListView):
    model = CardModel
    template_name = 'cardlist.html'


class CardDetailView(DetailView):
    model = CardModel
    template_name = 'carddetail.html'

# TODO попробовать перенести условие в формы 

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            if self.object.status in ('Ready', 'Done'):
                kwargs['form'] = HelperCardStatusUpdate(instance=self.object, user=self.request.user)
            else:
                kwargs['message'] = 'Task is not Ready'
        
        elif self.request.user == self.object.implementor:
            if self.object.status != 'Done':
                kwargs['form'] = HelperCardStatusUpdate(instance=self.object, user=self.request.user)
            else:
                kwargs['message'] = 'Task is complete'
        else:
            kwargs['denied'] = True
        return kwargs

class CardCreateView(LoginRequiredMixin, CreateView):
    model = CardModel
    form_class = CardCreateForm
    template_name = 'cardcreate.html'
    success_url = reverse_lazy('cards:cardlist')

    def get_form_kwargs(self):
        kwargs = super(CardCreateView, self).get_form_kwargs()
        kwargs['implementor'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
    

class CardUpdateView(IsCreatorOrSuperUserCheck, UpdateView):
    model = CardModel
    form_class = CardUpdateForm
    template_name = 'cardcreate.html'
    success_url = reverse_lazy('cards:cardlist')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user.is_superuser
        return kwargs

    # def get_form_class(self):
    #     if self.request.user.is_superuser:
    #         self.form_class = AdminCardUpdateForm
    #     else:
    #         self.form_class = UserCardUpdateForm
    #     return super().get_form_class()
    

class CardDeleteView(IsSuperUser, DeleteView):
    model = CardModel
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('cards:cardlist')

    def form_valid(self, form):
        messages.success(self.request, "The task was deleted successfully.")
        return super(CardDeleteView,self).form_valid(form)
    

# View for changing card status
class CardStatusUpdate(BaseUpdateView):
    http_method_names = ['post']
    model = CardModel
    form_class = CardStatusUpdate
    success_url = reverse_lazy('cards:cardlist')

    def get_form_kwargs(self):
        kwargs = super(CardStatusUpdate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    


class CardListAPI(generics.ListCreateAPIView):
    queryset = CardModel.objects.all()
    serializer_class = CardSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
