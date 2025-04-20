from django.shortcuts import render,get_object_or_404, redirect
from .models import Automezzo, ManutenzioneMezzi, CartaCarburante,Rifornimento, MagazzinoMezzo
from django.views.generic import FormView, ListView
from .forms import NuovomezzoForm, NuovoInterventoForm,CarburanteForm,CartaCarburanteForm, AggiornaMezzo
from django.contrib import messages
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model, get_user
import datetime
from django.utils import timezone
from logistica.models import Products



def nuovomezzo(request):
    form=NuovomezzoForm(request.POST, request.FILES)
    if request.method=='POST':
        form=NuovomezzoForm(request.POST, request.FILES)
        if form.is_valid():
            obj=form.save()
            prodotti=Products.objects.all()
            for a in prodotti:
                MagazzinoMezzo.objects.create(mezzo=obj, prodotto=a).save()
            return redirect('automezzi:elenco-mezzi')
        else:
            form=NuovomezzoForm()
    return render(request,'automezzi/nuovo-mezzo.html',{'form':form} )


def aggiornamezzo(request,pk):
    mezzo=get_object_or_404(Automezzo, pk=pk)
    form=AggiornaMezzo(instance=mezzo)
    if request.method=='POST':
        form=AggiornaMezzo(request.POST, instance=mezzo)
        if form.is_valid():
            form.save()
            return redirect('automezzi:elenco-mezzi')
    return render(request, 'automezzi/nuovo-mezzo.html', {'form':form})
    

    
def elencomezzi(request):
    mezzi=Automezzo.objects.all()
    return render(request,'automezzi/elenco-mezzi.html', {'mezzi':mezzi})

def vedimezzo(request, pk):
    mezzo=Automezzo.objects.get(pk=pk)
    return render(request, 'automezzi/scheda-mezzo.html', {'c':mezzo})



class NuovoIntervento(FormView):
    template_name='automezzi/nuovo-intervento.html'
    form_class=NuovoInterventoForm
    i_instance=None
    
      
    def get_success_url(self):
        return self.request.path
    
    def get_queryset(self):
        return ManutenzioneMezzi.objects.all()
    

    def form_valid(self, form):
        self.i_instance=form.save()
        messages.add_message(self.request, messages.INFO, f'Nuovo intervento: {self.i_instance.data_intervento} - {self.i_instance.mezzo.targa} - {self.i_instance.intervento} è stato inserito con successo')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        self.object_list = self.get_queryset()
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)


    
def elencointerventi(request):
    interventi=ManutenzioneMezzi.objects.all()
    return render(request,'automezzi/elenco-interventi.html', {'interventi':interventi})

def vediintervento(request, pk):
    intervento=ManutenzioneMezzi.objects.get(pk=pk)
    return render(request, 'automezzi/scheda-intervento.html', {'c':intervento})

def vediprodottimezzo(request,pk):
    mezzo=Automezzo.objects.get(pk=pk)
    
    return render(request, 'automezzi/giacenzemezzo.html',{'mezzo':mezzo})

#carburante!!!!!!!!!!!!!!!!!!!!!!

def nuovacartacarburante(request):
    form=CartaCarburanteForm(request.POST)
    if request.method=='POST':
        form=CartaCarburanteForm(request.POST)
        if form.is_valid():
            form.save()
        form = CartaCarburanteForm()
    return render(request,'automezzi/nuovacarta.html',{'form':form})

def rifornimento(request):
    form=CarburanteForm(request.POST)
    if request.method=='POST':
        form=CarburanteForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            user=request.user
            importo=request.POST['importo']
            carta=request.POST['carta']
            mezzo=request.POST['mezzo']
            mezzo=Automezzo.objects.get(pk=mezzo)
            carta=CartaCarburante.objects.get(pk=carta)
            if carta.residuo == carta.limite:
                scala=carta.limite-float(importo)
                carta.residuo=scala
                obj.residuo=scala
                carta.save()
                obj.save()
            elif carta.residuo<carta.limite:
                scala=carta.residuo-float(importo)
                carta.residuo=scala
                carta.save()
                obj.residuo=scala
                obj.save()
            return redirect('automezzi:vedicartacarburante')
        form = CarburanteForm()
    return render(request,'automezzi/rifornimento.html',{'form':form})

def vedicartacarburante(request):
    carta=Rifornimento.objects.order_by('-data')[:15]
    return render(request, 'automezzi/elencorifornimenti.html', {'carta':carta})

