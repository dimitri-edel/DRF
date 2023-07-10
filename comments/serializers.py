from rest_framework import serializers
from .models import *


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

    def get_is_owner(self, obj):
        # The request object has been passed as a parameter to the constructor
        # in the views
        request = self.context['request']
        # Return True if the user is the owner of the object
        return request.user == obj.owner

    class Meta:
        model = Comment
        fields = [
            'id',
            'owner',
            'created_at',
            'updated_at',
            'post',
            'content',
            'is_owner',
            'profile_id',
            'profile_image',
        ]

    
class CommentDetailSerializer(CommentSerializer):
    post = serializers.ReadOnlyField(source="post.id")
