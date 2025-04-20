from .models import Products,Warehouse,Install,Order
from django import forms
from anagrafica.models import Azienda,Privati,Filiali
from automezzi.models import Automezzo, MagazzinoMezzo

class DateInput(forms.DateInput):
    input_type = "date"
    
class ProdottoForm(forms.ModelForm):
    class Meta:
        model=Products
        fields=('__all__')
        labels={
            'prezzo':'Prezzo per singolo articolo'
        }
        
        
        
class OrderForm(forms.ModelForm):
    class Meta:
        model=Order
        exclude=('ricevuto','pdf','data_ricezione', 'articoli_ricevuti', 'pagato')
        widgets={
            'data_arrivo_ordine':DateInput(),
            
        }
        
class RicevimentoOrdine(forms.ModelForm):
    class Meta:
        model=Order
        fields=('articoli_ricevuti','data_ricezione','note')
        widgets={
            'note':forms.Textarea(),
            'data_ricezione':DateInput()
            
        } 
        labels={
            'articoli_ricevuti':'Articoli ricevuti (inserire solo il numero di articoli effettivamente ricevuti, al netto di riserve)',
            'note':'Indicare qui eventuali riserve o confermare che l\'ordine sia stato ricevuto regolarmente'
        }
        
        
class EntrataMerciForm(forms.ModelForm):
    quantità=forms.FloatField(min_value=0, required=True, label={'Quantità ricevuta':'quantità'})
    class Meta:
        model=Warehouse
        exclude=('ordine','data_uscita', 'giacenza','prodotto')  
        widgets={
            'data_entrata':DateInput()
        }      
        
        
class Primainstallazione(forms.ModelForm):
    prodotto=forms.ModelChoiceField(queryset=Products.objects.all(), to_field_name='pk')
    azienda=forms.ModelChoiceField(queryset=Azienda.objects.filter(installato=False))
    privati=forms.ModelChoiceField(queryset=Privati.objects.filter(installato=False))
    class Meta:
        model=Install
        fields=('__all__')
        widgets={
            'data_installazione':DateInput()
        }
        
class InstallForm(forms.ModelForm):
    mezzo=forms.ModelChoiceField(queryset=Automezzo.objects.all(), to_field_name='targa')
    class Meta:
        model=Install
        fields=('mezzo','azienda', 'privato', 'filiale', 'data_installazione', 'prodotto','quantità', 'cartelli', 'totale_postazioni','note')
        widgets={
            'data_installazione':DateInput()
        }
        labels={
            'quantità':'Quantità prodotto utilizzato'
        }
        
        
class AggiornaInstallazione(forms.ModelForm):
    mezzo=forms.ModelChoiceField(queryset=Automezzo.objects.all(), to_field_name='targa')

    class Meta:
        model=Install
        fields=('data_installazione', 'quantità', 'cartelli', 'totale_postazioni', 'note')
        labels={
            'data_installazione':'Data Aggiornamento',
            'quantità':'Indicare solo il numero di prodotti aggiunti',
            'cartelli':'Indicare il numero di cartelli totali presenti, non solo quelli aggiunti',
            'totale_postazioni':'Indicare il numero di postazioni totali, non solo quelle aggiunte'
        }
        widgets={
            'data_installazione':DateInput()
        }


class MagazzinoMezzoForm(forms.ModelForm):
    class Meta:
        model=MagazzinoMezzo
        fields=('__all__')
        
        
class Carico(forms.Form):
    prodotto=forms.ModelChoiceField(queryset=Products.objects.all().order_by('nome_prodotto'))
    quantita=forms.FloatField()
    
