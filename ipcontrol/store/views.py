from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Store, Pdv
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.messages import constants
import re
default_ip =r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$"

def validate_ip(ip):
    return re.match(default_ip,ip)

def new_store(request):
    if request.method == "POST":
    
        name = request.POST.get('name')
        concentrator = request.POST.get('ipconc')
        gateway = request.POST.get('gateway')
        details = request.POST.get('details')
        
        
        if not name:
            messages.add_message(request, constants.WARNING, 'O campo nome não pode ser vazio.')
            return redirect('/new_store')
        
        store = Store.objects.filter(name = name.upper())
    
        if store:
            messages.add_message(request, constants.WARNING, 'Loja com esse nome já cadastrada.')
            return redirect('/new_store')
        

        if not concentrator:
            messages.add_message(request, constants.WARNING, 'O campo concentrador não pode ser vazio.')
            return redirect('/new_store')
        if not gateway:
            messages.add_message(request, constants.WARNING, 'O campo gateway não pode ser vazio.')
            return redirect('/new_store')
        
        if not validate_ip(concentrator):
            messages.add_message(request, constants.WARNING, 'Campo concentrador inválido.')
            return redirect('/new_store')
        
        if not validate_ip(gateway):
            messages.add_message(request, constants.WARNING, 'Campo gateway inválido.')
            return redirect('/new_store')



        store = Store(name = name.upper(),
                    concentrator=concentrator,
                    gateway=gateway,
                    details=details)

        store.save()
        messages.add_message(request, constants.SUCCESS, 'Nova loja criada com sucesso!')
    return render(request, 'new_store.html')

def stores(request):
    stores = Store.objects.all().order_by('name')
    size_pdvs = Pdv.objects.all().count()
    number_stores = {}
    
    for store in stores:
        list_pdv = Pdv.objects.filter(store_id=store.id)
        number_stores[store.id] = len(list_pdv)
    
   # print(number_stores[38])
    
    filter_name = request.GET.get('name')
    if filter_name:
        stores = stores.filter(name__icontains=filter_name)

    return render(request, 'stores.html',{'stores': stores, 'number_stores': number_stores, 'size_pdvs': size_pdvs})

def delete_store(request,id):
    store = Store.objects.get(id=id)
    store.delete()
    messages.add_message(request, constants.SUCCESS, 'Loja deletada com Sucesso!')

    return redirect('/stores')

def edit_store(request,id):
    store = Store.objects.get(id=id)
    
    if request.method == "POST":
        name = request.POST.get('name')
        concentrator = request.POST.get('ipconc')
        gateway = request.POST.get('gateway')
        details = request.POST.get('details')

        if not name:
            messages.add_message(request, constants.WARNING, 'O campo nome não pode ser vazio.')
            return redirect(f'/edit_store/{store.id}')
        
        

        if not concentrator:
            messages.add_message(request, constants.WARNING, 'O campo concentrador não pode ser vazio.')
            return redirect(f'/edit_store/{store.id}')
        if not gateway:
            messages.add_message(request, constants.WARNING, 'O campo gateway não pode ser vazio.')
            return redirect(f'/edit_store/{store.id}')
        
        if not validate_ip(concentrator):
            messages.add_message(request, constants.WARNING, 'Campo concentrador inválido.')
            return redirect(f'/edit_store/{store.id}')
        
        if not validate_ip(gateway):
            messages.add_message(request, constants.WARNING, 'Campo gateway inválido.')
            return redirect(f'/edit_store/{store.id}')

        store.name = name
        store.concentrator = concentrator
        store.gateway = gateway
        store.details = details
        
        store.save()
        return redirect(f'/store/{store.id}')


    return render(request, 'edit_store.html',{ 'store': store})


def store(request, id):
    store = get_object_or_404 (Store, id=id)
    pdvs = Pdv.objects.filter(store_id = id)


    return render(request, 'store.html',{'store':store, 'logo':'logo-empresa/logo-superso.png', 'pdvs': pdvs})

def new_pdv(request):
    if request.method == 'GET':
        raise Http404()

    id_store = request.POST.get('id-store')
    nfce = request.POST.get('nfce')
    ip = request.POST.get('ip')

    #Vaidando os campos
    if not nfce:
        messages.add_message(request, constants.WARNING, 'O campo NFCE não pode ser vazio.')
        return redirect(f'/store/{id_store}')
    
    if not nfce.isdigit():
       messages.add_message(request, constants.WARNING, 'Insira apenas números no campo NFCE.')
       return redirect(f'/store/{id_store}')

    if not ip:
        messages.add_message(request, constants.WARNING, 'O formato do campo IP é inválido.')
        return redirect(f'/store/{id_store}')
    
    if not validate_ip(ip):
            messages.add_message(request, constants.WARNING, 'Campo IP inválido.')
            return redirect(f'/store/{id_store}')
    
    pdv = Pdv(nfce = nfce,
            ip = ip,
            store_id = id_store)

    nfce_filter = Pdv.objects.filter(store_id = id_store).filter(nfce = nfce)
    if nfce_filter:
        messages.add_message(request, constants.WARNING, f'NFCE {nfce} já cadastrado!')
        return redirect(f'/store/{id_store}')
    pdv.save()
    messages.add_message(request, constants.SUCCESS, 'Novo pdv adicionado com Sucesso!')
    return redirect(f'/store/{id_store}')

def delete_pdv(request, id_store,id_pdv):
    pdv = Pdv.objects.filter(id=id_pdv)

    pdv.delete()
    return redirect(f'/store/{id_store}')


def pdvs(request):
    store_list = Store.objects.all().order_by('name').values()
    # Verifica se já foi cadastrado uma loja
    if not store_list:
        return HttpResponse('CADASTRE UM LOJA PRIMEIRO')
    id_default = store_list[0]['id']
    pdv_list = []
    id_store = request.GET.get('store') or id_default
    #pdv_list = Pdv.objects.filter(store_id = id_store).order_by('nfce').values()
    if id_store:
        pdv_list = Pdv.objects.filter(store_id = id_store).order_by('nfce').values()
        id_store = int(id_store)
    


    return render(request,'pdvs.html',{'stores': store_list,
            'pdvs': pdv_list, 'store_selected': id_store, 'number_pdvs' : len(pdv_list)})
