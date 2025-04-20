from django import forms 
from .models import Servizio, Distinte,Recupero
from contratti.models import Contratto
from anagrafica.models import Azienda, Filiali
from logistica.models import Products,Warehouse




class DateInput(forms.DateInput):
    input_type = "date"
    
class Radioselect(forms.RadioSelect):
    input_type='radio'
    
class caricaFile(forms.ModelForm):
    class Meta:
        models=Servizio
        fields=('pdf',)
    
class ScegliCliente(forms.ModelForm):
    ragioneSociale=forms.ModelChoiceField(queryset=Azienda.objects.all())
    class Meta:
        model=Azienda
        fields=('ragioneSociale',)
           
    
class ServizioAziende(forms.ModelForm):
    class Meta:
        model=Servizio
        fields=('contratto','filiali','data_espletazione','altro_luogo',
                 'prezzo','incasso','Tiposervizio', 'prodotto', 'note','orario_inizio')        
    
        widgets={
            'data_espletazione': DateInput(),
            'orario_inizio' : forms.TimeInput(attrs={'type': 'time'}),
            'orario_fine':  forms.TimeInput(attrs={'type': 'time'}),
            'magazzino':forms.MultipleChoiceField(),
            }
        labels={
            'contratto':'Contratto',
            'filiali':'Filiale',
            'altro_luogo':'Luogo diverso',
            'incasso': 'Da Incassare',
            'magazzino': 'Prodotti da utilizzare',
            'prezzo':'Importo da incassare alla fine del servizio',
            'orario_inizio':'Appuntamento ore:',
            }
        
    def __init__(self, *args, azienda=None, **kwargs):
        super().__init__(*args, **kwargs)
        if azienda:
                self.fields['filiali'].queryset = Filiali.objects.filter(anaFiliale=azienda)        
        
class ServizioPrivati(forms.ModelForm):
    class Meta:
        model=Servizio
        exclude=['azienda', 'filiali', 'espletato','pdf', 'luogo_effettivo',
                 'contratto', 'inespl', 
                 'importo_incassato','data_chiusura','incasso']
        widgets={
            
            'data_espletazione': DateInput(),
            'orario_inizio' : forms.TimeInput(attrs={'type': 'time'}),
            'orario_fine':  forms.TimeInput(attrs={'type': 'time'}),}
        labels={
            'privati':'Cliente',
            'orario_inizio':'Appuntamento ore:'
        }
        
        
class DistinteForm(forms.ModelForm):
    servizio=forms.ModelMultipleChoiceField(queryset=Servizio.objects.filter(inespl=False), required=False)
    recupero=forms.ModelMultipleChoiceField(queryset=Recupero.objects.filter(chiuso=False), required=False)
    
    class Meta:
        model=Distinte 
        exclude=('azienda','filiale', 'privato','chiusura')
        widgets={
            'data':DateInput(),
        }
        labels={
            'servizio': 'Servizi da Espletare',
            'user':'Operatore'
        }
        
        
        
class salvaconferma(forms.ModelForm):
    class Meta:
        model=Servizio
        fields=('pdf',)  
    
class chiudirecupero(forms.ModelForm):
    class Meta:
        model=Recupero
        fields=('chiuso',)
        labels={
            'chiuso':'Chiudi recupero solo se veramente incassato per il totale, in caso contrario lascia in bianco e comunicalo in ufficio'
        }
class chiudiservizio(forms.ModelForm):
    quantità=forms.FloatField()
    class Meta:
        model=Servizio
        fields=('importo_incassato','note', 'espletato','prodotto','quantità','data_chiusura')
        widgets={
            'data_chiusura': DateInput(),
            
        }
        labels={
            'incasso':'Spuntare la casella solo in caso di incasso completo, in caso di incasso parziale e non incassato indicare nella casella sottostante l importo mancante.',
            'importo_incassato':"Indicare l'importo incassato",
            'prodotto':'Prodotto utilizzato per il servizio',
            'quantità':'Prodotto consumato per il servizio (indicare nr pezzi o litri)'
        }
        
from contabilità.models import NumeroCassa
        
class chiudidistinta(forms.ModelForm):
    cassa=forms.ModelChoiceField(queryset=NumeroCassa.objects.all())
    class Meta:
        model=Distinte
        fields=('cassa','chiusura',)
        labels={
            'cassa': 'Scegli cassa destinazione incassi'
        }



class cercaForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False)

    class Meta:
        model=Servizio
        fields=('azienda','privati','Tiposervizio','export_to_CSV')
        

class servizidelmese(forms.Form):
    cliente=forms.ModelChoiceField(queryset=Azienda.objects.all(), required=False)             

    data_inizio=forms.DateField(widget=DateInput)
    data_fine=forms.DateField(widget=DateInput)