from django.urls import path
from . import views
urlpatterns = [
    # paths for categories
    path('', views.dashboard, name='dashboard'),
    path('categories/', views.categories, name='categories'),
    path('categories/search', views.search_categories, name='search_categories'),
    path('categories/add', views.add_categories, name='add_categories'),
    path('categories/edit/<int:pk>', views.edit_categories, name='edit_categories'),    
    
    # paths for posts
    path('posts/', views.posts, name="posts"),
    path('posts/add/', views.add_posts, name="add_posts"),
    path('posts/search_posts/', views.search_posts, name="search_posts"),
    path('posts/filter/<int:category_id>/', views.filter_by_category, name='filter_by_category'),
    path('posts/edit/<int:pk>/', views.edit_posts, name="edit_posts"),
    path('posts/delete/<int:pk>/', views.delete_posts, name="delete_posts"),

    # path for users
    path('users/', views.users, name="users"),
    path('users/add/', views.add_users, name="add_users"),
    path('users/search/', views.search_users, name='search_users'),
    path('users/edit/<int:pk>/', views.edit_user, name="edit_user"),
    path('users/userprofile/<int:pk>/', views.userprofile, name="userprofile"),


   path('comments/', views.comments, name="comments"),
   path('comments/search', views.search_comments, name="search_comments"),
   path('manage_comment/<int:comment_id>/', views.manage_comment, name='manage_comments'),
   path('comments/delete/<int:pk>/', views.delete_comment, name='delete_comment'),
   
]