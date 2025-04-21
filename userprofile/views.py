from django.shortcuts import render, redirect
from .forms import UserProfileForm, ProfileForm, ManageCategoryForm 
from .models import Profile
from blogs.models import Category

def userprofile(request):
    user = request.user
    profile = user.profile  # Assuming a OneToOneField between User and Profile

    return render(request, 'user_profile/userprofile.html', {
        'user': user,
        'user_profile': profile  # Pass the profile to the template
    })

def editprofile(request):
    user = request.user
    profile = user.profile  # Get the user's profile

    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)  # Handle file uploads
 
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()  # Save the user data (username, email, etc.)
            profile_form.save()  # Save the profile picture
            return redirect('userprofile')  # Redirect to the user's profile page after saving
    else:
        user_form = UserProfileForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'user_profile/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def managecategory(request):
    user_profile = request.user.profile

    print("Available categories:", Category.objects.all())  # Debugging line

    if request.method == 'POST':
        form = ManageCategoryForm(request.POST, instance=user_profile)

        if 'categories' not in request.POST or not request.POST.getlist('categories'):
            user_profile.categories.clear()
            return redirect('userprofile')

        if form.is_valid():
            form.save()
            return redirect('userprofile')

    else:
        form = ManageCategoryForm(instance=user_profile)

    return render(request, 'user_profile/managecategory.html', {'form': form})



from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import PasswordChangeForm

def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data.get('current_password')
            new_password = form.cleaned_data.get('new_password')

            # Verify current password
            if not request.user.check_password(current_password):
                form.add_error('current_password', 'Current password is incorrect.')
            else:
                # Change password
                request.user.set_password(new_password)
                request.user.save()

                # Update session to keep the user logged in
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Your password has been successfully changed!')
                return redirect('home')  # Replace 'home' with the name of your home view
    else:
        form = PasswordChangeForm()

    return render(request, 'user_profile/change_password.html', {'form': form})



