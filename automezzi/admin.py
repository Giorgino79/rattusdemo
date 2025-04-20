from django.contrib import admin
from .models import Automezzo, ManutenzioneMezzi, CartaCarburante, Rifornimento, MagazzinoMezzo

admin.site.register(Automezzo)
admin.site.register(ManutenzioneMezzi)
admin.site.register(CartaCarburante)
admin.site.register(Rifornimento)
admin.site.register(MagazzinoMezzo)
