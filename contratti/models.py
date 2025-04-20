from django.db import models
from anagrafica.models import Azienda

class Contratto(models.Model):
    
    class TypeChoices(models.TextChoices):
        CASH='pagamento immediato', 'pagamento immediato'
        TRENTA='30 giorni data fattura fine mese','30 giorni data fattura fine mese'
        SESSANTA='60 giorni data fattura fine mese','60 giorni data fattura fine mese'
        NOVANTA='90 giorni data fattura fine mese','90 giorni data fattura fine mese'
        
    class ServizioChoices(models.TextChoices):
        derattizzazione='derattizzazione', 'derattizzazione'
        deblattizzazione='deblattizzazione', 'deblattizzazione'
        deformicazione='deformicazione', 'deformicazione'
        giardinaggio='giardinaggio', 'giardinaggio'
        disinfestazione='disinfestazione','disinfestazione'
        rimozione_guano='rimozione guano','rimozione_guano'
        rimozione_carcasse='rimozione_carcasse', 'rimozione_carcasse'
        mosche='mosche', 'mosche'
        antitarlo='antitarlo', 'antitarlo'
    
    class Frequenza(models.TextChoices):
        settimanale='settimanale','settimanale'
        bisettimanale='bisettimanale','bisettimanale'
        mensile='mensile','mensile'
        bimestrale='bimestrale','bimestrale'
        trimestrale='trimestrale','trimestrale'
        quadrimestrale='quadrimestrale','quadrimestrale'
        semestrale='semestrale', 'semestrale'
    
    nome_contratto=models.CharField(max_length=100, blank=True, null=True)
    anagrafica=models.ForeignKey(Azienda, on_delete=models.CASCADE, related_query_name='contratto')
    data=models.DateField(auto_now_add=True)
    tipo_servizio=models.CharField(max_length=50, choices=ServizioChoices.choices)
    prezzo=models.FloatField()
    area_coperta=models.IntegerField(blank=True,null=True)
    condomini=models.IntegerField(blank=True,null=True)
    frequenza=models.CharField(max_length=30, choices=Frequenza.choices)
    pagamento=models.CharField(max_length=50, choices=TypeChoices.choices)
    note=models.CharField(max_length=4000,blank=True, null=True)
    inizio_validità=models.DateField(blank=True, null=True)
    scadenza_contratto=models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.anagrafica.ragioneSociale} - {self.nome_contratto}'
    
    
    
    
    