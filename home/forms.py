from django  import forms
from .models import Messaggio
from django.contrib.auth import get_user_model


class MessaggioForm(forms.ModelForm):
    class Meta:
        model=Messaggio
        exclude=('mittente',)