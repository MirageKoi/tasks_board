from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CardModel

class CardListView(ListView):
    model = CardModel
    template_name = 'cardlist.html'


class CardDetailView(DetailView):
    model = CardModel
    template_name = 'carddetail.html'


class CardCreateView(LoginRequiredMixin, CreateView):
    model = CardModel
    fields = ['title', 'text', 'category', 'implementor']
    template_name = 'cardcreate.html'
    success_url = reverse_lazy('cards:cardlist')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

