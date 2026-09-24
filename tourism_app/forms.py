from django import forms
from .models import Review, TripInquiry

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['user_name', 'user_email', 'rating', 'title', 'comment']
        widgets = {
            'user_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name',
                'required': 'required'
            }),
            'user_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email Address',
                'required': 'required'
            }),
            'rating': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Review Headline (e.g., Unforgettable sunset & peaceful vibe!)'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience, tips for visitors, best photo spots...',
                'required': 'required'
            }),
        }


class TripInquiryForm(forms.ModelForm):
    class Meta:
        model = TripInquiry
        fields = ['name', 'email', 'phone', 'destination_state', 'destination_place', 'travel_date', 'travelers_count', 'budget_range', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address', 'required': 'required'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone / WhatsApp Number', 'required': 'required'}),
            'destination_state': forms.Select(attrs={'class': 'form-select'}),
            'destination_place': forms.Select(attrs={'class': 'form-select'}),
            'travel_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'travelers_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 50, 'value': 2}),
            'budget_range': forms.Select(
                choices=[
                    ('Budget (Under ₹10,000)', 'Budget (Under ₹10,000)'),
                    ('Moderate (₹10,000 - ₹25,000)', 'Moderate (₹10,000 - ₹25,000)'),
                    ('Luxury (₹25,000 - ₹50,000)', 'Luxury (₹25,000 - ₹50,000)'),
                    ('Ultra-Luxury (₹50,000+)', 'Ultra-Luxury (₹50,000+)'),
                ],
                attrs={'class': 'form-select'}
            ),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tell us about your trip plans, duration, special requirements...'}),
        }
