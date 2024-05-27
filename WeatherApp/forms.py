from django.forms import ModelForm, TextInput
from .models import City

class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ["name"]
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control col-sm-12',  # Added col-sm-4 for a smaller input box
                'placeholder': 'City Name'
            })
        }
