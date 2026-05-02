from django import forms


class CheckoutForm(forms.Form):
    customer_name = forms.CharField(
        label='Full name',
        max_length=140,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    customer_email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )
