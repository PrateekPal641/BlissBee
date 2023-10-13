# serializers.py

from rest_framework import serializers
from .models import Feeling, Material

class FeelingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feeling
        fields = '__all__'

class MaterialSerializer(serializers.ModelSerializer):
    feelings = FeelingSerializer(many=True, read_only=True)

    class Meta:
        model = Material
        fields = '__all__'
