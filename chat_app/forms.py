from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput,
    )


    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username','email', 'password1', 'password2', 'img')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data
    
class EmailChangeForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email']

    def update(self, user):
        user.email = self.cleaned_data['email']
        user.save()

class UsernameChangeForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username']

    def update(self, user):
        user.username = self.cleaned_data['username']
        user.save()

class ImgChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['img']
