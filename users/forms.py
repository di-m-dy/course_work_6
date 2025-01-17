from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from users.models import User


class FormControlMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(FormControlMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')



class LoginForm(FormControlMixin, AuthenticationForm):
    class Meta:
        fields = ('email', 'password')



class ProfileForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone')
