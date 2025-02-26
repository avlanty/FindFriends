from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    member = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "member", "content", "created_at"]

        def get_user(self, obj):
            return {'username': obj.user.username}