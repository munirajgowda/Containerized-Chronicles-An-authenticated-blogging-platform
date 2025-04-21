from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import Blogs, Category, Comment
from gtts import gTTS
import os
from django.conf import settings
from django.db.models import Q
from django.contrib.auth import get_user_model
from userprofile.models import Profile

# Path to save the audio files
AUDIO_PATH = os.path.join(settings.BASE_DIR, 'static', 'audio')

# Ensure the audio directory exists
if not os.path.exists(AUDIO_PATH):
    os.makedirs(AUDIO_PATH)

# Function to generate and save audio for a blog post
def generate_audio(blog):
    text_to_read = f"Title: {blog.title}. Short Description: {blog.short_description}. Content: {blog.blog_body}"
    tts = gTTS(text=text_to_read, lang='en')
    audio_file_path = os.path.join(AUDIO_PATH, f'blog_{blog.id}_En.mp3')
    tts.save(audio_file_path)
    return audio_file_path


# Blog posts by category
def posts_by_category(request, category_id):
    posts = Blogs.objects.filter(status='published', category=category_id)
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        return redirect('home')
    
    context = {
        'posts': posts,
        'category': category
    }
    return render(request, 'posts_by_category.html', context)


# Blog details page
def blogs(request, slug):
    # Retrieve the specific blog post
    single_post = get_object_or_404(Blogs, slug=slug, status='published')
    
    # Get related posts based on category (excluding the current post)
    related_posts = Blogs.objects.filter(category=single_post.category).exclude(id=single_post.id)[:4]  # Adjust number of related posts
    
    # Handle new comment submission
    if request.method == "POST":
        comment = Comment(user=request.user, blog=single_post, comment=request.POST['comment'])
        comment.save()
        return HttpResponseRedirect(request.path_info)

    comments = Comment.objects.filter(blog=single_post)
     
    context = {
        'single_post': single_post,
        'comments': comments,
        'comment_count': comments.count(),
        'related_posts': related_posts  # Pass related posts to the template
    }
    return render(request, 'blogs.html', context)



# search Functionality
def search(request):
    keyword = request.GET.get('keyword', '').strip()  # Ensure keyword is non-empty
    if keyword:
        blogs = Blogs.objects.filter(
            Q(title__icontains=keyword) |
            Q(short_description__icontains=keyword) |
            Q(blog_body__icontains=keyword),
            status='published'  # Only fetch published blogs
        )
    else:
        blogs = Blogs.objects.none()  # No results if keyword is empty

    context = {
        'blogs': blogs,
        'keyword': keyword
    }
    return render(request, 'search.html', context)



# Play or generate audio for the blog
def play_audio(request, blog_id):
    blog = get_object_or_404(Blogs, id=blog_id, status='published')

    # Path to the pre-generated audio file
    audio_file_path = os.path.join(AUDIO_PATH, f'blog_{blog_id}.mp3')

    # Check if the audio file exists
    if not os.path.exists(audio_file_path):
        # If the audio file doesn't exist, generate it dynamically
        try:
            generate_audio(blog)
        except Exception as e:
            return HttpResponse(f"Error generating audio: {str(e)}", status=500)

    # Serve the audio file
    if os.path.exists(audio_file_path):
        with open(audio_file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='audio/mp3')
            response['Content-Disposition'] = f'inline; filename="blog_{blog_id}.mp3"'
            return response
    else:
        return HttpResponse("Audio file not found", status=404)




def author_details(request, author_id, blog_slug):
    """
    Display author details in a card format.
    """
    User = get_user_model()
    author = get_object_or_404(User, id=author_id)

    # Fetch the profile picture or use a default
    profile_picture = getattr(author.profile, 'profile_picture', None)
    profile_picture_url = (
        profile_picture.url if profile_picture else "https://img.icons8.com/?size=100&id=0PXqKKGn88m8&format=png&color=000000"
    )

    # Count the number of posts uploaded by the author
    posts_uploaded = Blogs.objects.filter(author=author).count()

    context = {
        'author': author,
        'profile_picture_url': profile_picture_url,
        'blog_slug': blog_slug,  # Pass the slug of the blog
        'posts_uploaded': posts_uploaded,  # Pass the number of posts uploaded
    }
    return render(request, 'author_details.html', context)


def author_posts(request, username):
    author = get_object_or_404(get_user_model(), username=username)
    posts = Blogs.objects.filter(author=author)

    context = {
        'author': author,
        'posts': posts,
    }
    return render(request, 'author_posts.html', context)
