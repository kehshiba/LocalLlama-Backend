from rest_framework import serializers

from .models import ChatOutput


class ChatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChatOutput
        fields = ('title', 'description')
