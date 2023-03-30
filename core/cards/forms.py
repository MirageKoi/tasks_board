from django import forms
from django.contrib.auth import get_user_model

from .models import CardModel

User = get_user_model()

class CardCreateForm(forms.ModelForm):

    class Meta:
        model = CardModel
        exclude = ['creator', 'status', 'created', 'updated']

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('implementor', None)
        super(CardCreateForm, self).__init__(*args, **kwargs)
        if current_user:
            self.fields['implementor'].queryset = User.objects.filter(id=current_user.id)


class AdminCardUpdateForm(forms.ModelForm):

    class Meta:
        model = CardModel
        fields = ['text', 'implementor']


class UserCardUpdateForm(forms.ModelForm):

    class Meta:
        model = CardModel
        fields = ['text']

# TODO обьеденить два вержних класса в один. добавить условие IF admin or not. Попробовать через инит. Добавить имлементора

class UserCardStatusUpdate(forms.ModelForm):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In progress', 'In progress'),
        ('In QA', 'In QA'),
        ('Ready', 'Ready'),
    ]

    status = forms.ChoiceField(choices=[('In progress', 'In progress'), ('In QA', 'In QA'), ('Ready', 'Ready')], required=False)
   
    class Meta:
        model = CardModel
        fields = ['status']

