from rest_framework import serializers
from .models import Follower
from django.db import IntegrityError


class FollowerSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    followed_name = serializers.ReadOnlyField(source="followed.username")

    class Meta:
        model = Follower
        fields = [
            'id',
            'owner',
            'followed',
            'created_at',
            'followed_name',
        ]


    def create(self, validated_data):
    # Prevent duplicate likes
        try:
            return super().create(validated_data)
        except IntegrityError:
        # Due to models.Likes.unique_together['followed', 'owner]
        # if the user attmpts to add a like twice an IntegrityError will be rasied        
            raise serializers.ValidationError({
                'detail': 'Cannot follow the same user twice!'
            })
