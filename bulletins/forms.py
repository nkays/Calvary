from django import forms

from .models import Bulletin


class BulletinForm(forms.ModelForm):
    class Meta:
        model = Bulletin
        fields = [
            'date',
            'title',
            'section1',
            'section2',
            'section3',
            'section4',
            'section5',
            'section6',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # add bootstrap classes to all textareas
        for field in ['section1', 'section2', 'section3', 'section4', 'section5', 'section6']:
            self.fields[field].widget = forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            )
