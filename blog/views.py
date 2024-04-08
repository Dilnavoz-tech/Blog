from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from telegram import Bot

from blog.models import Post, Comment, Like
from blog.serializers import PostSerializer, CommentSerializer


@api_view(http_method_names=['GET'])
def get_posts(request):
    posts = PostSerializer(Post.objects.all(), many=True)

    return Response(
        status=status.HTTP_200_OK,
        data=posts.data

    )


@api_view(http_method_names=['Get'])
def get_by_id(request, pk):
    post = get_object_or_404(Post, id=pk)

    post_response = PostSerializer(post)
    comments = post.comment_set.all()
    comment_serializer = CommentSerializer(comments, many=True)

    data = {
        'post': post_response.data,
        'comments': comment_serializer.data
    }

    return Response(data, status=status.HTTP_200_OK)


@api_view(http_method_names=['Post'])
def create_post(request):
    data = request.data
    post = Post.objects.create(title=data['title'], description=data['description'],
                               image='/media/future4.jpg')
    posts = PostSerializer(post)

    return Response(
        status=status.HTTP_200_OK,
        data=posts.data
    )
@api_view(http_method_names=['PUT', 'PATCH'])
def update_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    post_data = request.data
    post_serializer = PostSerializer(instance=post, data=post_data)
    if post_serializer.is_valid():
        post_serializer.save()
        return Response(data=post_serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(data=post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(http_method_names=['DELETE'])
def delete_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['POST'])
def create_comment(request):
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH'])
def update_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    comment_data = request.data

    comment_serializer = CommentSerializer(instance=comment, data=comment_data)
    if comment_serializer.is_valid():
        comment_serializer.save()

        return Response(data=comment_serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(data=comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


TELEGRAM_BOT_TOKEN = '6725176067:AAFYwaMgrBHuvq8V-iwzLOLNRjIVH1UYIBU'


@api_view(['POST'])
def notify_telegram(request):
    if request.method == 'POST':
        post_data = request.data
        post_title = post_data.get('title')

        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        message = f'New post added: {post_title}'
        bot.send_message(chat_id='@ba_test_123_bot (https://t.me/ba_test_123_bot)', text=message)

        return Response({'message': 'Notification sent to Telegram'})
    else:
        return Response({'error': 'Invalid request method'})


@api_view(['POST'])
def create_like(request, post_id):
    if request.method == 'POST':
        try:
            like = Like.objects.create(post_id=post_id)
            like.save()
            return Response({'message': 'Like created successfully'})
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=404)
    else:
        return Response({'error': 'Invalid request method'})





