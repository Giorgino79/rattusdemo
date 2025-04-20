from django import forms 
from .models import Contratto


class DateInput(forms.DateInput):
    input_type = "date"

class ContrattoForm(forms.ModelForm):
    class Meta:
        model=Contratto
        fields=('__all__')
        widgets={
            'data':DateInput(),
            'inizio_validità':DateInput(),
            'scadenza_contratto':DateInput()
        }
        
        def clean_nome_contratto(self):
            nome_contratto=self.cleaned_data.get('nome_contratto')
            if not nome_contratto:
                raise forms.ValidationError('Campo obbligatorio')
            for instance in Contratto.objects.all():
                if instance.nome_contratto==nome_contratto:
                    raise forms.ValidationError(nome_contratto + 'già esistente, variare il nome')
            return nome_contratto