from django.urls import path

from blog.views import get_posts, get_by_id, create_post, create_comment, delete_post, update_post, update_comment, \
    delete_comment, create_like

urlpatterns = [
    path('get/', get_posts),
    path('get/<int:pk>/', get_by_id),
    path('create/posts/', create_post),
    path('update/posts/<int:pk>/', update_post),
    path('delete/posts/<int:pk>/', delete_post),
    path('create/comments/', create_comment),
    path('update/comments/<int:pk>/', update_comment),
    path('delete/comments/<int:pk>/', delete_comment),
    path('posts/<int:post_id>/like/', create_like),

]