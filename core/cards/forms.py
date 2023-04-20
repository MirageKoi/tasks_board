from django import forms
from django.contrib.auth import get_user_model

from .models import CardModel

User = get_user_model()


class CardCreateForm(forms.ModelForm):

    class Meta:
        model = CardModel
        exclude = ['creator', 'status', 'created', 'updated']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('implementor', None)
        super(CardCreateForm, self).__init__(*args, **kwargs)
        if not user.is_superuser:
            self.fields['implementor'].queryset = User.objects.filter(
                id=user.id)


class CardUpdateForm(forms.ModelForm):
    class Meta:
        model = CardModel
        fields = ['text', 'implementor']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if not user:
            del self.fields['implementor']


class HelperCardStatusUpdate(forms.ModelForm):

    class Meta:
        model = CardModel
        fields = ['status']

    def __init__(self, user, *args, **kwargs):
        user = user
        super().__init__(*args, **kwargs)
        if user.is_superuser:
            self.fields['status'].choices = [
                ('Ready', 'Ready'),
                ('Done', 'Done'),
            ]
        else:
            self.fields['status'].choices = [
                ('In progress', 'In progress'),
                ('In QA', 'In QA'),
                ('Ready', 'Ready'),
            ]


class CardStatusUpdate(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        user = kwargs.pop('user', None)
        super(CardStatusUpdate, self).__init__(*args, **kwargs)

        if user and user.is_superuser:
            self.fields['status'].choices = [
                ('Ready', 'Ready'),
                ('Done', 'Done'),
            ]
        else:
            self.fields['status'].choices = [
                ('In progress', 'In progress'),
                ('In QA', 'In QA'),
                ('Ready', 'Ready'),
            ]

    class Meta:
        model = CardModel
        fields = ['status']
