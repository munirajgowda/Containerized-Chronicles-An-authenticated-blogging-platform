from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from blogs.models import Category


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    as_admin = forms.BooleanField(required=False, initial=False)
    interests = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'as_admin', 'interests']


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email")

    def clean(self):
        username_or_email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if '@' in username_or_email:
            try:
                user = User.objects.get(email=username_or_email)
                username = user.username
            except User.DoesNotExist:
                raise forms.ValidationError("Invalid email or password")
        else:
            username = username_or_email
        
        self.cleaned_data['username'] = username
        return super().clean()



class EmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))


class OTPVerificationForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email'}), required=True)
    otp = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'otp'}), required=True)


class PasswordResetForm(forms.Form):
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'new_password'}),
        label="New Password",
        required=True
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'confirm_password'}),
        label="Confirm New Password",
        required=True
    )


