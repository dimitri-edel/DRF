from rest_framework import serializers
from .models import *


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        # The request object has been passed as a parameter to the constructor
        # in the views
        request = self.context['request']
        # Return True if the user is the owner of the object
        return request.user == obj.owner

    class Meta:
        model = Profile
        fields = [
            'id',
            'owner',
            'created_at',
            'updated_at',
            'name',
            'content',
            'image',
            'is_owner',
        ]