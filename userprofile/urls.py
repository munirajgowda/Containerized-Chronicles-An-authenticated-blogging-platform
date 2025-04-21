from django.urls import path
from . import views
urlpatterns = [
    path('', views.userprofile, name='userprofile'),
    path('edit/', views.editprofile, name='editprofile'),
    path('managecategory/', views.managecategory, name='managecategory'),
    path('change-password/', views.change_password, name='change_password'),
    
]