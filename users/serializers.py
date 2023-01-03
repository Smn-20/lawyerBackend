from rest_framework import serializers 

from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



class CaseSerializer(serializers.ModelSerializer):
    proof = serializers.FileField(
        max_length = 1000000,
        allow_empty_file = False,
        write_only = True
    )
    class Meta:
        model = Case
        fields = '__all__'

class FirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firm
        fields = '__all__'

class LawyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lawyer
        fields = '__all__'
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['firm'] is not None:
            data['firm'] = FirmSerializer(
                Firm.objects.get(pk=data['firm'])).data 
        return data 

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

