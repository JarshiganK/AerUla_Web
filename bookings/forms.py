from django import forms

from .models import BookingRequest


class BookingRequestForm(forms.ModelForm):
    class Meta:
        model = BookingRequest
        fields = ['preferred_date', 'guests', 'notes']
        widgets = {
            'preferred_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'guests': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12}),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Accessibility, language, or timing notes',
            }),
        }

    def clean_guests(self):
        guests = self.cleaned_data['guests']
        if guests < 1 or guests > 12:
            raise forms.ValidationError('Guests must be between 1 and 12.')
        return guests
