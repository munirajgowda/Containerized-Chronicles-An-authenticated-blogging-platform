from django.shortcuts import render,redirect
from blogs.models import Category, Blogs, Comment
from . forms import CategoryForm, BlogPostForm
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from .forms import AddUserForm, EditUserForm, ManageCommentForm



def dashboard(request):
    category_counts = Category.objects.all().count()
    blogs_counts = Blogs.objects.all().count()
    context = {
        'category_counts':category_counts,
        'blogs_counts':blogs_counts
    }

    return render(request, 'dashboard/dashboard.html', context)


from django.db.models import Count

def categories(request):
    # Annotate each category with the count of blogs
    categories = Category.objects.annotate(blogs_counts=Count('blogs'))
    context = {
        'categories': categories  # Pass the annotated categories to the template
    }
    return render(request, 'dashboard/categories.html', context)



def add_categories(request):
    if request.method=="POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    form = CategoryForm()
    context = {
        'form':form
    }
    return render(request, 'dashboard/add_categories.html', context)



def edit_categories(request,pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method=="POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    form = CategoryForm(instance=category)
    context = {
        'form':form,
        'category':category
    }
    return render(request, 'dashboard/edit_categories.html',context)



def posts(request):
    # Fetch blogs uploaded by the logged-in user
    my_blogs = Blogs.objects.filter(author=request.user)
    categories = Category.objects.all()
    
    # Fetch all blogs if the user is a superuser
    all_blogs = Blogs.objects.all() if request.user.is_superuser else None

    context = {
        'my_blogs': my_blogs,
        'blogs': all_blogs,  # For superusers
    }
    return render(request, 'dashboard/posts.html', context)



def add_posts(request):
    if request.method=="POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title)
            post.save()
            print("Success")
            return redirect('posts')
        else:
            print(form.errors)

    form = BlogPostForm()
    context = {
        'form':form
    }
    return render(request, 'dashboard/add_posts.html', context)


def edit_posts(request,pk):
    post = get_object_or_404(Blogs, pk=pk)
    if request.method=="POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title)
            post.save()
            return redirect('posts')
    form = BlogPostForm(instance=post)
    context={
        'form':form,
        'post':post
    }
    return render(request, 'dashboard/edit_post.html',context)



def delete_posts(request,pk):
    post = get_object_or_404(Blogs, pk=pk)
    post.delete()
    return redirect('posts')



def users(request):
    users = User.objects.all()
    context = {
        'users':users
    }
    return render(request, 'dashboard/users.html', context)

def add_users(request):
    if request.method=="POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')
    form = AddUserForm()
    context = {
        'form':form
    }
    return render(request, 'dashboard/add_users.html',context)



def edit_user(request,pk):
    user = get_object_or_404(User, pk=pk)
    if request.method =="POST":
         form = EditUserForm(request.POST, instance= user)
         if form.is_valid():
             form.save()
             return redirect('users')
    form = EditUserForm(instance=user)
    context = {
        'form':form,
        'user':user
    }
    return render(request, 'dashboard/edit_user.html',context)

def userprofile(request, pk):
    user = get_object_or_404(User, pk=pk)
    context = {
        'user':user
    }
    return render(request, 'dashboard/profile.html', context)


def comments(request):
    if request.user.is_superuser:
        # Superuser sees all comments
        comments = Comment.objects.select_related('user', 'blog').all()
    else:
        # Regular users see comments only on their blogs
        user_blogs = Blogs.objects.filter(author=request.user)
        comments = Comment.objects.select_related('user', 'blog').filter(blog__in=user_blogs)

    context = {'comments': comments}
    return render(request, 'dashboard/comments.html', context)


def manage_comment(request, comment_id):
    # Retrieve the comment by id
    comment = get_object_or_404(Comment, id=comment_id)

    # If the form is submitted, handle the POST request
    if request.method == 'POST':
        form = ManageCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('comments')  # Redirect to the comments list after saving
    else:
        form = ManageCommentForm(instance=comment)

    return render(request, 'dashboard/manage_comments.html', {'form': form, 'comment_id': comment_id})


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('comments') 


def search_posts(request):
    keyword = request.GET.get('keyword', '').strip()
    search_scope = request.GET.get('scope', '')  # Determine the block (my_blogs or all_blogs)

    my_blogs = Blogs.objects.filter(author=request.user)  # User's blogs
    blogs = Blogs.objects.all() if request.user.is_superuser else None  # All blogs (only for superusers)

    # Filtering logic
    if keyword:
        if search_scope == 'my_blogs':
            my_blogs = my_blogs.filter(title__icontains=keyword)
        elif search_scope == 'all_blogs' and request.user.is_superuser:
            blogs = blogs.filter(title__icontains=keyword)

    context = {
        'my_blogs': my_blogs,
        'blogs': blogs,
        'search_scope': search_scope,
    }
    return render(request, 'dashboard/posts.html', context)



def filter_by_category(request, category_id):
    category = Category.objects.get(id=category_id)
    my_blogs = Blogs.objects.filter(category=category, author=request.user) if request.user.is_authenticated else []
    blogs = Blogs.objects.filter(category=category) if request.user.is_superuser else []
    categories = Category.objects.all()

    context = {
        'my_blogs': my_blogs,
        'blogs': blogs,
        'categories': categories,
        'search_scope': 'my_blogs' if request.user.is_authenticated else 'all_blogs',
    }
    return render(request, 'dashboard/posts.html', context)



def search_comments(request):
    keyword = request.GET.get('keyword', '').strip()  # Search keyword
    search_scope = request.GET.get('scope', 'my_blogs')  # Default scope is 'my_blogs'
    user = request.user

    # Initialize queryset based on scope
    if search_scope == 'my_blogs':
        # Comments for blogs authored by the current user
        comments = Comment.objects.filter(blog__author=user)
    elif search_scope == 'all_blogs' and user.is_superuser:
        # All comments (for superuser only)
        comments = Comment.objects.all()
    else:
        comments = Comment.objects.none()

    # Apply the blog title search filter if a keyword is provided
    if keyword:
        comments = comments.filter(blog__title__icontains=keyword)

    context = {
        'comments': comments,
        'search_scope': search_scope,
        'keyword': keyword,  # Pass the keyword back to the template
    }
    return render(request, 'dashboard/comments.html', context)



def search_categories(request):
    keyword = request.GET.get('keyword', '').strip()
    search_scope = request.GET.get('scope', '')  # Determine the block (my_blogs or all_blogs)

    my_blogs = Blogs.objects.filter(author=request.user)  # User's blogs
    blogs = Blogs.objects.all() if request.user.is_superuser else None  # All blogs (only for superusers)

    # Fetch categories and apply filtering logic
    categories = Category.objects.all()  # Correct usage of the model manager

    if keyword:
        categories = categories.filter(category_name__icontains=keyword)

    # Filtering logic for blogs
    if keyword:
        if search_scope == 'my_blogs':
            my_blogs = my_blogs.filter(title__icontains=keyword)
        elif search_scope == 'all_blogs' and request.user.is_superuser:
            blogs = blogs.filter(title__icontains=keyword)

    context = {
        'my_blogs': my_blogs,
        'blogs': blogs,
        'categories': categories,  # Pass categories to the template
        'search_scope': search_scope,  # Pass scope to the template
    }
    return render(request, 'dashboard/categories.html', context)



def search_users(request):
    keyword = request.GET.get('keyword', '').strip()  # Get the search keyword from the request
    users = User.objects.all()  # Fetch all users initially

    if keyword:
        # Search for users by first name, last name, username, or email
        users = users.filter(
            first_name__icontains=keyword
        ) | users.filter(
            last_name__icontains=keyword
        ) | users.filter(
            username__icontains=keyword
        ) | users.filter(
            email__icontains=keyword
        )

    context = {
        'users': users,  # Pass the filtered users to the template
    }
    return render(request, 'dashboard/users.html', context)