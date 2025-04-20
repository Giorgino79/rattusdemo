from django.shortcuts import render,redirect
from .models import Contratto
from .forms import ContrattoForm

def nuovocontratto(request):
    form=ContrattoForm(request.POST)
    if request.method=='POST':
        form=ContrattoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home:home')
    else:
        ContrattoForm()
    return render(request, 'contratti/nuovocontratto.html', {'form':form})

def elencocontratti(request):
    contratti=Contratto.objects.all().order_by('anagrafica')
    return render(request, 'contratti/elencocontratti.html', {'contratti':contratti})
    
    
def vedicontratti(request,pk):
    contratto=Contratto.objects.get(pk=pk)
    return render(request, 'contratti/vedicontratto.html', {'c':contratto})
    

def modificacontratto(request,pk):
    contratto=Contratto.objects.get(pk=pk)
    form=ContrattoForm(instance=contratto)
    if request.method=='POST':
        form=ContrattoForm(request.POST, instance=contratto)
        if form.is_valid():
            form.save()
            return redirect('contratti:elencocontratti')
    else:
        ContrattoForm()
    return render(request,'contratti/modificacontratto.html', {'form':form})

def eliminacontratto(request,pk):
    contratto=Contratto.objects.get(pk=pk)
    if request.method=='POST':
        contratto.delete()
        return redirect('contratti:elencocontratti')
    return render(request, 'contratti/eliminacontratti.html', {'c':contratto})
