from django.db import IntegrityError
from rest_framework import serializers
from .models import *


class LikesSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Likes
        fields = [
            'id',
            'owner',  
            'created_at',
            'post',          
        ]

    def create(self, validated_data):
    # Prevent duplicate likes
        try:
            return super().create(validated_data)
        except IntegrityError:
        # Due to models.Likes.unique_together['post', 'owner]
        # if the user attmpts to add a like twice an IntegrityError will be rasied        
            raise serializers.ValidationError({
                'detail': 'Cannot like the same post twice!'
            })
