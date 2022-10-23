from django import forms

from magazine.models import Companies, Profile


class BargainingForms(forms.ModelForm):
    class Meta:
        model = Companies
        fields = ['title', 'companies', 'comments', 'money']

        widgets = {
            'companies': forms.TextInput(attrs={'class': 'form-control'}),
            'money': forms.NumberInput(attrs={'class': 'form-control'})
        }


class ProfileForms(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['car', 'phone', 'address']

        widgets = {
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
        }

