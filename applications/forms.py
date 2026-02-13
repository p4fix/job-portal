from django import forms
from .models import Application


def validate_pdf(value):
    if not value.name.lower().endswith('.pdf'):
        raise forms.ValidationError('Only PDF files are allowed for resume upload.')


class ApplicationForm(forms.ModelForm):
    resume = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
        validators=[validate_pdf]
    )

    class Meta:
        model = Application
        fields = ['resume']


class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
