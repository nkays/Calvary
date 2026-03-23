from django import forms
from staff.validators import validate_blocked_email
from .models import LandingPageEntry

class LandingPageEntryModelForm(forms.ModelForm):
    # name = forms.CharField(max_length=100)
    # email = forms.EmailField(validators=[validate_blocked_email])
    email2 = forms.EmailField(label="Confirm Email", validators=[validate_blocked_email])

    class Meta:
        model = LandingPageEntry
        fields = ['name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Your Name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Your Email'})
        self.fields['email2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Your Email'})

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        email2 = cleaned_data.get("email2")
        if email != email2:
            self.add_error('email2', "Emails must match.")
            # raise forms.ValidationError("Emails must match.")
        return cleaned_data



class LandingPageForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(validators=[validate_blocked_email])
    email2 = forms.EmailField(label="Confirm Email", validators=[validate_blocked_email])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Your Name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Your Email'})
        self.fields['email2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Your Email'})

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        email2 = cleaned_data.get("email2")
        if email != email2:
            self.add_error('email2', "Emails must match.")
            # raise forms.ValidationError("Emails must match.")
        return cleaned_data

