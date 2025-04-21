from django.urls import path
from . import views

urlpatterns = [
    path('<int:category_id>/', views.posts_by_category, name='posts_by_category'),
    path('blogs/<slug:slug>/', views.blogs, name='post_detail'),
    path('<int:blog_id>/play_audio/', views.play_audio, name='play_audio'),
    path('author/<int:author_id>/<slug:blog_slug>/', views.author_details, name='author-details'),
    path('author/<str:username>/posts/', views.author_posts, name='author_posts'),
]
