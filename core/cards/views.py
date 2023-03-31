from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from django.views.generic.edit import BaseUpdateView, FormView, ProcessFormView, FormMixin

from .forms import AdminCardUpdateForm, CardCreateForm, UserCardUpdateForm, UserCardStatusUpdate,  AdminCardStatusUpdate, CardStatusUpdate
from .models import CardModel
from .permissions import IsCreatorOrSuperUserCheck, IsSuperUser, IsCreator

from django.contrib.auth.mixins import UserPassesTestMixin



class CardListView(ListView):
    model = CardModel
    template_name = 'cardlist.html'


class CardDetailView(DetailView):
    model = CardModel
    template_name = 'carddetail.html'

# TODO попробовать перенести условие в формы 

    def get_context_data(self, **kwargs):
        if self.request.user.is_superuser:
            kwargs['form'] = AdminCardStatusUpdate(instance=self.object)
        else:
            kwargs['form'] = UserCardStatusUpdate(instance=self.object)
        return super().get_context_data(**kwargs)


class CardCreateView(LoginRequiredMixin, CreateView):
    model = CardModel
    form_class = CardCreateForm
    template_name = 'cardcreate.html'
    success_url = reverse_lazy('cards:cardlist')

    def get_form_kwargs(self):
        kwargs = super(CardCreateView, self).get_form_kwargs()
        if not self.request.user.is_superuser:
            kwargs['implementor'] = self.request.user
        else:
            kwargs['implementor'] = None
        return kwargs

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
    

class CardUpdateView(UpdateView, IsCreatorOrSuperUserCheck):
    model = CardModel
    template_name = 'cardcreate.html'
    success_url = reverse_lazy('cards:cardlist')

    def get_form_class(self):
        if self.request.user.is_superuser:
            self.form_class = AdminCardUpdateForm
        else:
            self.form_class = UserCardUpdateForm
        return super().get_form_class()
    

class CardDeleteView(DeleteView, IsSuperUser):
    model = CardModel
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('cards:cardlist')

    def form_valid(self, form):
        messages.success(self.request, "The task was deleted successfully.")
        return super(CardDeleteView,self).form_valid(form)
    

class CardStatusUpdate(BaseUpdateView):
    http_method_names = ['post']
    model = CardModel
    form_class = CardStatusUpdate

    def get_form_kwargs(self):
        kwargs = super(CardStatusUpdate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    # def get_form_class(self):
    #     if self.request.user.is_superuser:
    #         self.form_class = AdminCardStatusUpdate
    #     else:
    #         self.form_class = UserCardStatusUpdate
    #     return super().get_form_class()
    
    def get_success_url(self):
        object_id = self.kwargs[self.pk_url_kwarg]
        return reverse_lazy('cards:detail', kwargs={'pk': object_id})
    