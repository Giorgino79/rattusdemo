from django.contrib import admin
from .models import Azienda, Filiali, Fornitori, Privati


admin.site.register(Azienda)
admin.site.register(Filiali)
admin.site.register(Fornitori)
admin.site.register(Privati)
