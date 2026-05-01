from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Review, Newsletter


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'example@mail.com'}),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': "Логін",
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Введіть логін'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

        self.fields['password1'].label = 'Пароль'
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'placeholder': 'Введіть пароль'}
        )
        self.fields['password1'].error_messages = {
            'required': 'Введіть пароль.',
        }

        self.fields['password2'].label = 'Підтвердження паролю'
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'placeholder': 'Повторіть пароль'}
        )
        self.fields['password2'].error_messages = {
            'required': 'Підтвердіть пароль.',
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Паролі не співпадають.')
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Такий логін вже зайнятий. Оберіть інший.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('Акаунт з таким email вже існує.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('user_name', 'rating', 'comment')
        labels = {
            'user_name': "Ваше ім'я",
            'rating': 'Оцінка (1–5)',
            'comment': 'Коментар',
        }
        widgets = {
            'user_name': forms.TextInput(attrs={'placeholder': "Як вас звати?"}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Поділіться враженнями...'}),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is not None and not (1 <= rating <= 5):
            raise forms.ValidationError('Оцінка повинна бути від 1 до 5.')
        return rating


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ('email',)
        labels = {'email': 'Email'}
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Ваш email'}),
        }