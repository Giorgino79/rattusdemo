from django  import forms
from .models import Azienda, Filiali, Fornitori, Privati



class AziendaForm(forms.ModelForm):
    class Meta:
        model=Azienda
        exclude=('installato',)
        labels={
            'ragioneSociale':'Ragione Sociale',
            'indSedeLegale':'Indirizzo',
            'cittaLegale': 'Città',
            'capLegale':'Cap',
            'Provincia':'Provincia',
            'PI':'Partita Iva',
            'CF':'Codice Fiscale',
            'CU':'Codice Univoco',
            'tipo': 'Tipo Azienda',
            'referente': 'Nome del Referente Principale (facoltativo)'
                }
    
    def clean(self):
        ragSoc=self.cleaned_data.get('ragioneSociale')
        
        azienda_ragSoc_exists=Azienda.objects.filter(ragioneSociale__iexact=ragSoc).exists()
         
        if azienda_ragSoc_exists:
            self.add_error('ragioneSociale','Questa ragione sociale già esiste, usare codice esistente o variare il nome')
        
        return self.cleaned_data
    
class FilialiForm(forms.ModelForm):
    anaFiliale=forms.ModelChoiceField(queryset=Azienda.objects.filter(tipo='Multifiliale'))
    class Meta:
        model=Filiali
        exclude=('installato',)
        labels={
            'anaFiliale': 'Seleziona Cliente',
            'nomeFiliale': 'Appellativo Filiale',
            'indFiliale': 'Indirizzo',
            'cittaFiliale':'Città',
            'capFiliale':'Cap',
            'telFiliale':'Telefono della filiale',
            'mailFiliale':'Mail della filiale',
            'referenteFiliale': 'Referente di filiale'
        }

class FornitoriForm(forms.ModelForm):
    class Meta:
        model=Fornitori
        fields=('__all__')
        labels={
            'ragioneSociale':'Ragione Sociale',
            'indSedeLegale':'Indirizzo',
            'cittaLegale': 'Città',
            'capLegale':'Cap',
            'Provincia':'Provincia',
            'PI':'Partita Iva',
            'CF':'Codice Fiscale',
            'CU':'Codice Univoco',
            'referente': 'Nome del Referente Principale (facoltativo)'
                }
    
    def clean(self):
        ragSoc=self.cleaned_data.get('ragioneSociale')
        
        azienda_ragSoc_exists=Fornitori.objects.filter(ragioneSociale__iexact=ragSoc).exists()
        
        if azienda_ragSoc_exists:
            self.add_error('ragioneSociale','Questa ragione sociale già esiste, usare codice esistente o variare il nome')
        
        return self.cleaned_data

class AggFornitoriForm(forms.ModelForm):
    class Meta:
        model=Fornitori
        fields=('__all__')
        labels={
            'ragioneSociale':'Ragione Sociale',
            'indSedeLegale':'Indirizzo',
            'cittaLegale': 'Città',
            'capLegale':'Cap',
            'Provincia':'Provincia',
            'PI':'Partita Iva',
            'CF':'Codice Fiscale',
            'CU':'Codice Univoco',
            'referente': 'Nome del Referente Principale (facoltativo)'
                }
 
class PrivatiForm(forms.ModelForm):
    class Meta:
        model=Privati
        exclude=('installato',)
        labels={
            'nome_cognome':'Nome e Cognome (inserire prima il cognome e dopo il nome)',
            'parente1':'Moglie',
            'parente2':'Altro Parente',
            'telefono_parente1':'Telefono Moglie',
            'telefono_parente2':'Telefono Altro Parente',
            
        }
    def clean(self):
        nomcog=self.cleaned_data.get('nome_cognome')
        
        azienda_nomcog_exists=Privati.objects.filter(nome_cognome__iexact=nomcog).exists()
        
        if azienda_nomcog_exists:
            self.add_error('nome_cognome','Questo privato già esiste, usare codice esistente o variare il nome')
        
        return self.cleaned_data
    
    
class AggiornaAzienda(forms.ModelForm):
    class Meta:
        model=Azienda
        fields=('__all__')
        labels={
            'ragioneSociale':'Ragione Sociale',
            'indSedeLegale':'Indirizzo',
            'cittaLegale': 'Città',
            'capLegale':'Cap',
            'Provincia':'Provincia',
            'PI':'Partita Iva',
            'CF':'Codice Fiscale',
            'CU':'Codice Univoco',
            'tipo': 'Tipo Azienda',
            'referente': 'Nome del Referente Principale (facoltativo)'
                }
    
class AggiornaFiliale(forms.ModelForm):
    class Meta:
        model =Filiali
        fields={'nomeFiliale': 'Nome Filiale',
            'indFiliale': 'Indirizzo Filiale',
            'cittaFiliale':'Città',
            'capFiliale': 'Cap',
            'telFiliale': 'Telefono',
            'referenteFiliale': 'Referente'}