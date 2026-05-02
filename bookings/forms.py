from django import forms

from .models import BookingRequest, Experience


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


class VendorExperienceForm(forms.ModelForm):
    includes_text = forms.CharField(
        label='What is included',
        required=False,
        help_text='Add one included item per line.',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Hands-on demonstration\nMaterials for the session\nTea or light refreshments',
        }),
    )

    class Meta:
        model = Experience
        fields = [
            'hut',
            'title',
            'slug',
            'host',
            'duration',
            'price',
            'currency',
            'summary',
            'includes_text',
        ]
        widgets = {
            'hut': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'host': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '2 hours'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'currency': forms.TextInput(attrs={'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
        help_texts = {
            'slug': 'Use lowercase words separated by hyphens, such as pottery-wheel-session.',
            'host': 'Public host, artisan, or collective name shown to visitors.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.includes:
            self.fields['includes_text'].initial = '\n'.join(self.instance.includes)

    def clean_includes_text(self):
        text = self.cleaned_data.get('includes_text', '')
        return [line.strip() for line in text.splitlines() if line.strip()]

    def save(self, commit=True):
        experience = super().save(commit=False)
        experience.includes = self.cleaned_data['includes_text']
        experience.is_published = False
        experience.status = Experience.STATUS_PREVIEW
        if commit:
            experience.save()
            self.save_m2m()
        return experience
