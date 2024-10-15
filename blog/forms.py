from django import forms
from blog.models import Blog


class FormControlMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class BlogForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'text', 'image', 'is_active')
