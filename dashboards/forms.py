from django import forms
from blogs.models import Category,Blogs, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields = '__all__'


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Blogs
        fields = ('title',  'blog_image', 'short_description', 'blog_body', 'category', 'status', 'is_featured')



class AddUserForm(UserCreationForm):
    class Meta:
        model=User
        fields = ('username','email','first_name','last_name','is_active','is_staff','is_superuser','groups','user_permissions')
        

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name','is_active','is_staff','is_superuser','groups','user_permissions')


class ManageCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('user', 'blog', 'comment')
