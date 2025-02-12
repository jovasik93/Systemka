from django import forms
from .models import Item
from django import forms
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['serial_number', 'owner', 'start_date', 'end_date', 'description',]



class UploadFileForm(forms.Form):
    file = forms.FileField(label="Выберите Exel файл")


class ItemEditForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['serial_number', 'owner', 'start_date', 'end_date', 'description']

class PasswordConfirmationForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")