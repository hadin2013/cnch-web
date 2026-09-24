from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import SchoolGroup, Student

User = get_user_model()

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label="First name", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}))
    last_name = forms.CharField(label="Last name", required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}))
    email = forms.EmailField(label="Email", required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    date_of_birth = forms.DateField(label="Date of birth" , required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Date of birth'}))
    address = forms.CharField(label="Address", max_length=1024 , required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Physical Address'}),)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'date_of_birth', 'address',  'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm your password'})

class LoginForm(forms.Form):
    username_or_email = forms.CharField(label="Username or Email", required=True, 
        widget=forms.TextInput(attrs={"type": "text", "class": "form-control", "placeholder": "Username or Email"}))
    password = forms.CharField(label="Password", required=True,
        widget=forms.PasswordInput(attrs={"type": "password", "class": "form-control", "placeholder": "Password"}),)
    remember_me = forms.BooleanField(label="Remember me", required=False, 
        widget=forms.CheckboxInput(attrs={"type": "checkbox", "class": "checkbox-control", "placeholder": "Password"}))

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label="Email", required=True, max_length=256, widget=forms.EmailInput(attrs={"type": "email"}))

class SchoolGroupForm(forms.ModelForm):
    class Meta:
        model = SchoolGroup
        fields = ['group_name', 'province', 'city', 'school_name', 'school_phone']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'national_id', 'phone_number', 'grade', 'major']

StudentFormSet = forms.formset_factory(StudentForm, extra=3, min_num=3, max_num=6, validate_min=True, validate_max=True)