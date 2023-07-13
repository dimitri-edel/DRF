from rest_framework import serializers
from .models import *
from followers.models import Follower


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # A method-field is comprised of get_<field-name> 
    # is_owner translates to get_is_owner(self, obj)
    is_owner = serializers.SerializerMethodField()
    # A method-field is comprised of get_<field-name>
    # following_id translates to get_following_id(self, oobj)
    following_id = serializers.SerializerMethodField()
    # Computed fields placed by annotate() in the view
    posts_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        # The request object has been passed as a parameter to the constructor
        # in the views
        request = self.context['request']
        # Return True if the user is the owner of the object
        return request.user == obj.owner

    def get_following_id(self, obj):
        # The request object has been passed as a parameter to the constructor
        # in the views
        request = self.context['request']
        user = request.user
        
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            return following.id if following else None
        return None

   
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
            'following_id',  
            'posts_count',
            'followers_count',
            'following_count',          
        ]