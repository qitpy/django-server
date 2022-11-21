from rest_framework import serializers
from core.models import (
    PortfolioMessage,
    PortfolioAccessFrequency,
)
class PortfolioAccessFrequencySerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioAccessFrequency
        fields = ['id_address']

class PortfolioMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioMessage
        fields = ['message', 'ip_address']
