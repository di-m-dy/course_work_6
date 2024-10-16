from django import forms
from newsletters.models import Newsletter, Client, Message


class FormControlMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

class NewsletterForm(FormControlMixin, forms.ModelForm):
    date_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
            'placeholder': 'Select a date and time'
        }),
        label='Время первой рассылки',
        required=True
    )
    class Meta:
        model = Newsletter
        fields = ['message', 'clients', 'period', 'date_time']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['clients'].queryset = Client.objects.filter(user=user)


class MessageForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = ('title', 'text')


class ClientForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = (
            'first_name',
            'last_name',
            'parent_name',
            'email',
            'comment'
        )
