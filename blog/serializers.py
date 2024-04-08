from rest_framework.serializers import ModelSerializer

from blog.models import Post, Comment


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'image', 'created_at')


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('post_id', 'name', 'message', 'created_at')