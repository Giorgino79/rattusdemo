from django import forms
from .models import Automezzo, ManutenzioneMezzi, CartaCarburante,Rifornimento

class DateInput(forms.DateInput):
    input_type = "date"

class NuovomezzoForm(forms.ModelForm):
    class Meta:
        model=Automezzo
        exclude=('data_alienazione','alienato')
        widgets= {'data_acquisto': DateInput(),
                  'data_revisione': DateInput(),
                  'data_alienazione': DateInput(),}
        
        def clean(self):
            targa=self.cleaned_data.get('targa')
            
            mezzo_targa_exists=Automezzo.objects.filter(ragioneSociale__iexact=targa).exists()
            
            if mezzo_targa_exists:
                self.add_error('targa','Questa targa già esiste, controllare elenco mezzi')
            
            return self.cleaned_data
        
class AggiungiProdottiMezzo(forms.ModelForm):
    class Meta:
        model=Automezzo
        exclude=('targa', 'marca','modello','foto','data_revisione', 'alimentazione','data_acquisto', 'valore_acquisto',
                 'data_alienazione','alienato','note')

class AggiornaMezzo(forms.ModelForm):
    class Meta:
        model=Automezzo
        exclude=('targa', 'marca','modello','data_revisione', 'alimentazione','data_acquisto', 'valore_acquisto',
                 'data_alienazione','alienato','note')

class NuovoInterventoForm(forms.ModelForm):
    class Meta:
        model=ManutenzioneMezzi
        fields=('__all__')
        widgets= {'data_intervento': DateInput(),
                  'ora':forms.TimeInput(attrs={'type': 'time'})
                  }
        
        
class CartaCarburanteForm(forms.ModelForm):
    class Meta:
        model=CartaCarburante
        fields=('__all__')

class CarburanteForm(forms.ModelForm):
    class Meta:
        model=Rifornimento
        fields=('__all__')
        

    
    