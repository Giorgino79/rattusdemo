
from servizi.models import Recupero
from django import forms
from servizi.models import Servizio
from anagrafica.models import Azienda
from .models import Banca, Cassa, Movimenti, FatturaAttiva, FatturaPassiva, NumeroCassa
from contratti.models import Contratto
from anagrafica.models import Fornitori
from logistica.models import Order
class DateInput(forms.DateInput):
    input_type = "date"


class NumeroCassaForm(forms.ModelForm):
    class Meta:
        model=NumeroCassa
        fields=('nome',)

class Mesata(forms.Form):
        cliente=forms.ModelChoiceField(queryset=Contratto.objects.all(), required=False)             
        ordini_fornitore=forms.ModelMultipleChoiceField(queryset=Order.objects.all(), required=False, to_field_name='fornitore_id')
        data_inizio=forms.DateField(widget=DateInput)
        data_fine=forms.DateField(widget=DateInput)

class Elencoserviziperfattura(forms.Form):
    cliente=forms.ModelChoiceField(queryset=Contratto.objects.all(), required=False)             
    fornitore=forms.ModelChoiceField(queryset=Fornitori.objects.all(), required=False)
    data_inizio=forms.DateField(widget=DateInput)
    data_fine=forms.DateField(widget=DateInput)
 

class FatturaAttivaForm(forms.ModelForm):
    class Meta:
        model=FatturaAttiva
        exclude=('data_pagamento','da_incassare', 'importoiva', 'totale','dare','avere')
        widgets={
            'data_fattura':DateInput(),
            'data_scadenza':DateInput()

        }


        
        
class FatturaPassivaForm(forms.ModelForm):
    ordini_acquisto=forms.ModelMultipleChoiceField(queryset=Order.objects.filter(pagato=False), required=False)
    class Meta:
        model=FatturaPassiva
        exclude=('da_pagare', 'avere','dare',)
        widgets={
            'data_fattura':DateInput(),
            'data_pagamento':DateInput()
        }


class RecuperoForm(forms.ModelForm):
    
    # servizio=forms.ModelChoiceField(queryset=Servizio.objects.filter(incasso=False).filter(espletato=True))
    class Meta:
        model=Recupero
        fields=('importo_da_recuperare', 'data', 'note', 'chiuso', 'data_chiusura')
        widgets={
            'data':forms.DateInput(attrs={'type':'date'}),
            'data_chiusura':forms.DateInput(attrs={'type':'date'})
        }        
        labels={
            'importo_da_recuperare':'Importo da recuperare in caso di variazioni, importo recuperato in caso di chiusura del recupero',
            'data':'Data concordata per il recupero',
            'data_chiusura':'Inserisci data di chiusura del recupero',
            'importo': 'Importo da recuperare',
            'chiuso':'chiudi il recupero'
        }

class Chiudirecupero(forms.ModelForm):
    class Meta:
        model=Recupero
        fields=('data','importo_da_recuperare','chiuso', )
        widgets={
            'data':DateInput()
        }
        labels={
            'importo':'Importo recuperato'
        }
        
class AggiornaRecupero(forms.ModelForm):
    class Meta:
        model=Recupero
        fields=('importo_da_recuperare', 'data', 'note', )
        widgets={
                'data':DateInput()

        }
        labels={
            'importo':'Importo da riscuotere'
        }

class BancaForm(forms.ModelForm):
    class Meta:
        model=Banca
        fields=('__all__')
        
class MovimentiForm(forms.ModelForm):
    fattura_passiva=forms.ModelChoiceField(queryset=FatturaPassiva.objects.filter(da_pagare=True), required=False)
    fattura_attiva=forms.ModelChoiceField(queryset=FatturaAttiva.objects.filter(da_incassare=True), required=False)
    class Meta:
        model=Movimenti
        fields=('__all__')
        widgets={
            'data':DateInput(),
        }
        

class Versa(forms.ModelForm):
    class Meta:
        model=Movimenti
        exclude=('fattura_attiva','fattura_passiva')
        widgets={
            'data':DateInput(),
        }
