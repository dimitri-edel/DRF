from rest_framework import serializers
from .models import *
# for created_at and updated_at fields
from django.contrib.humanize.templatetags.humanize import naturaltime

class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    # Make created_at look like: 3 days ago, 2 hours ago, etc.
    created_at = serializers.SerializerMethodField()
    # Make updated_at look like: 3 days ago, 2 hours ago, etc.
    updated_at = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
    # SerializeMethod of Field is_owner
        # The request object has been passed as a parameter to the constructor
        # in the views
        request = self.context['request']
        # Return True if the user is the owner of the object
        return request.user == obj.owner

    def get_created_at(self, obj):
    # SerialzeMethod for field created_at
        return naturaltime(obj.created_at)

    def get_updated_at(self, obj):
    # SerialzeMethod for field updated_at
        return naturaltime(obj.updated_at)


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
