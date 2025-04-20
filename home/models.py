from django.db import models
from django.utils.timezone import now

class Messaggio(models.Model):
    mittente = models.ForeignKey('dipendenti.Dipendente', related_name="messaggi_inviati", on_delete=models.CASCADE)
    destinatario = models.ForeignKey('dipendenti.Dipendente', related_name="messaggi_ricevuti", on_delete=models.CASCADE)
    testo = models.TextField()
    timestamp = models.DateTimeField(default=now)

    class Meta:
        ordering = ['timestamp']  # Ordina i messaggi in ordine cronologico

    def __str__(self):
        return f"{self.mittente} -> {self.destinatario}: {self.testo[:30]}" 