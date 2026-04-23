from django import forms
from .models import Review, Newsletter


RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]


class ReviewForm(forms.ModelForm):
    # Красиві зірочки замість поля 1..5
    rating = forms.TypedChoiceField(
        choices=RATING_CHOICES,
        coerce=int,
        widget=forms.RadioSelect(attrs={'class': 'star-rating-input'}),
        label="Ваша оцінка",
    )

    class Meta:
        model = Review
        fields = ['user_name', 'rating', 'comment']
        widgets = {
            'user_name': forms.TextInput(attrs={
                'placeholder': "Ваше ім'я",
                'class': 'form-input',
                'maxlength': 100,
            }),
            'comment': forms.Textarea(attrs={
                'placeholder': 'Поділіться враженнями від рослини...',
                'rows': 4,
                'class': 'form-input',
            }),
        }
        labels = {
            'user_name': "Ваше ім'я",
            'comment': "Коментар",
        }


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Введіть ваш email',
                'class': 'newsletter-input',
                'required': 'required',
            }),
        }
        labels = {
            'email': 'Email',
        }
