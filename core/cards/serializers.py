from rest_framework import serializers
from .models import CardModel

from django.contrib.auth import get_user_model

User = get_user_model()

class CardListSerializer(serializers.ModelSerializer):
    # title = serializers.ReadOnlyField()
    # status = serializers.ChoiceField(choices=[('Ready', 'Ready'), ('Done', 'Done')])
    creator = serializers.ReadOnlyField(source='creator.username')
    status = serializers.ReadOnlyField()
    # udpdated = serializers.ReadOnlyField()

    class Meta:
        model = CardModel
        fields = '__all__'

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(*args, instance, **kwargs)
        user = kwargs['context']['request'].user
        if not user.is_superuser:
            self.fields['implementor'].queryset = User.objects.filter(id=user.id)


class CardDetailSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField()
    creator = serializers.ReadOnlyField(source='creator.username')
    status = serializers.ReadOnlyField()
    text = serializers.ReadOnlyField()
    implementor = serializers.ReadOnlyField(source='implementor.username')

    class Meta:
        model = CardModel
        fields = '__all__'

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(*args, instance, **kwargs)
        user = kwargs['context']['request'].user
        if user.is_superuser:
            self.fields['text'] = serializers.CharField()
            if instance.status in ('Ready', 'Done'):
                self.fields['status'] = serializers.ChoiceField(choices=[('Ready', 'Ready'), ('Done', 'Done')])
        if not user.is_superuser:
            if instance.creator == user:
                self.fields['text'] = serializers.CharField()
            if instance.implementor == user:
                if instance.status in ('New', 'In progress', 'In QA', 'Ready'):
                    self.fields['status'] = serializers.ChoiceField(choices = [('In progress', 'In progress'), ('In QA', 'In QA'), ('Ready', 'Ready')])