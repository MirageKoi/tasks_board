from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, FormView)

from .forms import AdminCardUpdateForm, CardCreateForm, UserCardUpdateForm, UserCardStatusUpdate
from .models import CardModel
from .permissions import IsCreatorOrSuperUserCheck, IsSuperUser, IsCreator




class CardListView(ListView):
    model = CardModel
    template_name = 'cardlist.html'


class CardDetailView(DetailView, FormView):
    model = CardModel
    form_class = UserCardStatusUpdate
    template_name = 'carddetail.html'


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
    

class CardStatusUpdateUp(UpdateView):
    model = CardModel
    template_name = 'cardcreate.html'
    fields = ['status']
    success_url = reverse_lazy('cards:cardlist')

    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        return super().post(request, *args, **kwargs)
