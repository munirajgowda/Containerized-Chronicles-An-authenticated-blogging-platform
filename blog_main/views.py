from django.shortcuts import render, redirect
from blogs.models import Category, Blogs
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm, CustomAuthenticationForm
from django.contrib.auth.models import User
from userprofile.models import Profile
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.conf import settings
import random   
from django.contrib import messages
 

# Home View
def home(request):
    categories = Category.objects.all()  # Fetch all categories
    featured_post = Blogs.objects.filter(is_featured=True, status='published')  # Featured posts
    posts = Blogs.objects.filter(is_featured=False, status='published')  # Regular published posts

    interest_posts = []  # Default to an empty list

    if request.user.is_authenticated:
        try:
            user_profile = Profile.objects.get(user=request.user)  # Get the user's profile
            user_categories = user_profile.categories.all()  # Get categories of interest
            interest_posts = Blogs.objects.filter(category__in=user_categories, status='published')
        except Profile.DoesNotExist:
            pass  # Profile not found; proceed without interest_posts

    context = {
        'categories': categories,
        'featured_post': featured_post,
        'posts': posts,
        'interest_posts': interest_posts,
    }
    return render(request, 'home.html', context)

# Register View
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Create the user
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )

            # If "Register as Admin" is selected
            if form.cleaned_data['as_admin']:
                user.is_staff = True
                user.save()

            # Check if profile already exists
            profile, created = Profile.objects.get_or_create(user=user)

            # Assign selected categories to the profile
            selected_categories = form.cleaned_data.get('interests')
            if selected_categories:
                profile.categories.set(selected_categories)

            profile.save()
            return redirect('home')  # Redirect to login page
    else:
        form = RegistrationForm()
    context = {
        'form': form
    }

    return render(request, 'register.html', context)



# Login View

def login(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)
            if user is not None:
                Profile.objects.get_or_create(user=user)

                auth.login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Invalid email/username or password")
    else:
        form = CustomAuthenticationForm()
    
    context = {
        'form': form
    }
    return render(request, 'login.html', context)


# Logout View
def logout(request):
    auth.logout(request)
    return redirect('home')


# Simulate OTP storage
otp_storage = {}

def verify_otp(request):
    if request.method == "POST":
        if "send_otp" in request.POST:  # Handle sending OTP
            username_or_email = request.POST.get('username_or_email')
            
            # Check if input is an email or username
            if '@' in username_or_email:  # Likely an email
                user = User.objects.filter(email=username_or_email).first()
            else:  # Assume it's a username
                user = User.objects.filter(username=username_or_email).first()

            if user:
                email = user.email
                otp = send_otp_email(email)
                request.session['email'] = email  # Store email in session
                messages.success(request, f"OTP sent to {email}. Please verify.")
                return render(request, 'verify_otp.html', {"email": email, "otp_sent": True})
            else:
                messages.error(request, "No account found with that username or email address.")
        
        elif "verify_otp" in request.POST:  # Handle OTP verification
            email = request.session.get('email')
            entered_otp = request.POST.get('otp')

            if email and entered_otp == otp_storage.get(email):
                del otp_storage[email]  # Remove OTP after successful verification
                messages.success(request, "OTP Verified successfully. You can now reset your password.")
                return redirect('forgetpassword')
            else:
                messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'verify_otp.html')


def forgetpassword(request):
    if request.method == "POST":
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        email = request.session.get('email')  # Retrieve email from session

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match. Please try again.")
            return render(request, 'forgetpassword.html')

        if not email:
            messages.error(request, "Session expired. Please start the process again.")
            return redirect('password_reset')  # Redirect to the password reset start page

        user = User.objects.filter(email=email).first()
        if user:
            user.set_password(new_password)  # Update the user's password
            user.save()
            messages.success(request, "Password reset successfully. Please log in.")
            return redirect('login')
        else:
            messages.error(request, "User not found.")
            return redirect('password_reset')  # Redirect to the password reset start page

    return render(request, 'forgetpassword.html')






from django.core.mail import send_mail
from django.conf import settings
import random

# Secure storage (use a database for production)
otp_storage = {}

def send_otp_email(email):
    try:
        otp = str(random.randint(100000, 999999))
        otp_storage[email] = otp
        send_mail(
            subject="Your OTP for Password Reset",
            message=f"Your OTP is {otp}. Please use it to verify your identity.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
        print(f"OTP {otp} sent to {email}")
        return True
    except Exception as e:
        print(f"Failed to send OTP: {e}")
        return False



from .models import OtpToken
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail


def send_otp(request):
    if request.method == 'POST':
        user_email = request.POST["otp_email"]
        
        if get_user_model().objects.filter(email=user_email).exists():
            user = get_user_model().objects.get(email=user_email)
            otp = OtpToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
            
            
            # email variables
            subject="Email Verification"
            message = f"""
                                Hi {user.username}, here is your OTP {otp.otp_code} \n
                                it expires in 5 minute
                                """
            sender = "containerisedchronicles@gmail.com"
            receiver = [user.email, ]
        
        
            # send email
            send_mail(
                    subject,
                    message,
                    sender,
                    receiver,
                    fail_silently=False,
                )
            
            messages.success(request, "A new OTP has been sent to your email-address")
            return redirect("verify-email", username=user.username)

        else:
            messages.warning(request, "This email dosen't exist in the database")
            return redirect("resend-otp")
        
           
    context = {}
    return render(request, "verify_otp.html", context)
