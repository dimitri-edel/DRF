from rest_framework import serializers
from .models import *
from likes.models import Likes


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    # A method-field is comprised of get_<field-name>
    # following_id translates to get_like_id(self, oobj)
    like_id = serializers.SerializerMethodField()
    comments_count = serializers.ReadOnlyField()
    likes_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        # The request object has been passed as a parameter to the constructor
        # in the views
        request = self.context['request']
        # Return True if the user is the owner of the object
        return request.user == obj.owner

    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            likes = Likes.objects.filter(
                owner=user, post=obj
            ).first()
            return likes.id if likes else None
        return None

    # Validation method of the image size dimensions
    # ModelSerializer will look for methods named validate_<field_name>(self,  value)
    def validate_image(self, value):
        if value.size > 1024 * 1024 *2:
            raise serializers.ValidationError('Image size larger than 2MB!')

        if value.image.width > 4096:
            raise serializers.ValidationError('Image width larger than 4096px!')

        if value.image.height > 4096:
            raise serializers.ValidationError('Image height is larger than 4096px!')
        return value

    class Meta:
        model = Post
        fields = [
            'id',
            'owner',
            'created_at',
            'updated_at',
            'title',
            'content',
            'image',
            'is_owner',
            'profile_id',
            'profile_image',
            'image_filter',
            'like_id',
            'comments_count',
            'likes_count',
        ]