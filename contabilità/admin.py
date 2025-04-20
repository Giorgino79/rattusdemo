from django.contrib import admin
from .models import Cassa, Banca,BancaMovimenti, Movimenti,FatturaAttiva,FatturaPassiva, Versamenti

admin.site.register(Cassa)
admin.site.register(Banca)
admin.site.register(BancaMovimenti)
admin.site.register(Movimenti)
admin.site.register(FatturaPassiva)
admin.site.register(FatturaAttiva)
admin.site.register(Versamenti)
