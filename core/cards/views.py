from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.views.generic.edit import BaseUpdateView
from rest_framework import generics, permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .forms import (CardCreateForm, CardStatusUpdate, CardUpdateForm,
                    HelperCardStatusUpdate)
from .models import CardModel
from .permissions import (IsCreatorOrSuperUserCheck, IsImplementorOrReadOnly,
                          IsSuperUser)
from .serializers import CardDetailSerializer, CardListSerializer


class CardListView(ListView):
    model = CardModel
    template_name = 'card_list.html'


class CardDetailView(LoginRequiredMixin, DetailView):
    model = CardModel
    template_name = 'card_detail.html'

# TODO попробовать перенести условие в формы

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            if self.object.status in ('Ready', 'Done'):
                kwargs['form'] = HelperCardStatusUpdate(
                    instance=self.object, user=self.request.user)
            else:
                kwargs['message'] = 'Task is not Ready'

        elif self.request.user == self.object.implementor:
            if self.object.status != 'Done':
                kwargs['form'] = HelperCardStatusUpdate(
                    instance=self.object, user=self.request.user)
            else:
                kwargs['message'] = 'Task is complete'
        else:
            kwargs['denied'] = True
        return kwargs


class CardCreateView(LoginRequiredMixin, CreateView):
    model = CardModel
    form_class = CardCreateForm
    template_name = 'card_create.html'
    success_url = reverse_lazy('cards:cardlist')

    def get_form_kwargs(self):
        kwargs = super(CardCreateView, self).get_form_kwargs()
        kwargs['implementor'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class CardUpdateView(LoginRequiredMixin, IsCreatorOrSuperUserCheck, UpdateView):
    model = CardModel
    form_class = CardUpdateForm
    template_name = 'card_update.html'
    success_url = reverse_lazy('cards:cardlist')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user.is_superuser
        return kwargs


class CardDeleteView(LoginRequiredMixin, IsSuperUser, DeleteView):
    model = CardModel
    template_name = 'card_confirm_delete.html'
    success_url = reverse_lazy('cards:cardlist')

    def form_valid(self, form):
        messages.success(self.request, "The task was deleted successfully.")
        return super(CardDeleteView, self).form_valid(form)


class CardStatusUpdate(LoginRequiredMixin, BaseUpdateView):
    http_method_names = ['post']
    model = CardModel
    form_class = CardStatusUpdate
    success_url = reverse_lazy('cards:cardlist')

    def get_form_kwargs(self):
        kwargs = super(CardStatusUpdate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


'''========================================================================================================'''


class CardListAPI(generics.ListCreateAPIView):
    queryset = CardModel.objects.all()
    serializer_class = CardListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['status']
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class CardDetailAPI(generics.RetrieveUpdateAPIView):
    queryset = CardModel.objects.all()
    serializer_class = CardDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsImplementorOrReadOnly]


class CardDeleteAPI(generics.DestroyAPIView):
    queryset = CardModel.objects.all()
    serializer_class = CardListSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
