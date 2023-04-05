from rest_framework import serializers
from .models import CardModel



class CardSerializer(serializers.ModelSerializer):
    # snippets = serializers.HyperlinkedIdentityField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = CardModel
        fields = '__all__'