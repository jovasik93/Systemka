from django import forms
from .models import Item
from django import forms
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['serial_number', 'owner', 'start_date', 'end_date', 'description',]
        widgets = {
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            'owner': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class UploadFileForm(forms.Form):
    file = forms.FileField(label="Выберите Exel файл")


class ItemEditForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['serial_number', 'owner', 'start_date', 'end_date', 'description']
        widgets = {
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            'owner': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class PasswordConfirmationForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")