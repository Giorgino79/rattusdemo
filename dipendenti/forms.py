from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Dipendente, Giornata 
from django.contrib.auth import get_user_model
from contabilità.forms import DateInput

class DipendenteForm(UserCreationForm):
    pass
    # class Meta:
    #     model =get_user_model()
    #     fields=('username','email','password', 'first_name', 'last_name', 'date_joined', 'groups',
    #         'livello','indirizzo','CF', 'carta_d_identità',
    #         'patente_di_guida', 'posizione_inail', 'posizione_inps', 'foto_carta_identità','foto_codice_fiscale',
    #         'foto_patente', 'foto_dipendente','all1','all2','all3','all4','note'
    #     )        
        
    # def save(self, commit=True):
    #     user=super(DipendenteForm, self).save()
    #     return user
    

class Mensilità(forms.Form):
    dipendente=forms.ModelChoiceField(queryset=Dipendente.objects.all())
    data_inizio=forms.DateField(widget=DateInput)    
    data_fine=forms.DateField(widget=DateInput)
    
    
class InizioGiornata(forms.ModelForm):
    
    class Meta:
        model=Giornata
        fields=('ora_inizio_mattina', 'mezzo')
        widgets= {
                 'ora_inizio_mattina' : forms.TimeInput(attrs={'type': 'time'}),

        }
        
class GiornataForm(forms.ModelForm):
    class Meta:
        model=Giornata
        fields=('ora_fine_mattina','ora_inizio_pomeriggio', 'ora_fine_pomeriggio','chiudi_giornata')
        widgets= {
                 'ora_fine_mattina' : forms.TimeInput(attrs={'type': 'time'}),
                 'ora_inizio_pomeriggio' : forms.TimeInput(attrs={'type': 'time'}),
                 'ora_fine_pomeriggio' : forms.TimeInput(attrs={'type': 'time'}),

        }
    
 