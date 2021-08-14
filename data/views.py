from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json
from .models import *
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from .filters import SPPSiswaFilter, SiswaFilter
from django.contrib import messages
import midtransclient
from django.conf import settings
import uuid
from django.contrib.auth.decorators import login_required
from .decorators import tolakhalaman_ini, ijinkan_pengguna, pilihan_login
from django.views.generic import View
from django.db.models import Sum
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.views.generic import ListView
from io import BytesIO
from django.template.loader import get_template
from django.views import View


def pdflap(request):
    # kelas = Kelas.objects.get(id=pk)
    # laporan = kelas.siswa_set.all()
    lapor = SppItem.objects.values('sppsiswa__siswa__nisn', 'sppsiswa__siswa__nama', 'sppsiswa__siswa__namakls__namakls').annotate(sppsiswa__lunas_count=Count('spp__bulan', filter=Q(sppsiswa__lunas=True)),not_sppsiswa__lunas_count=Count('spp__bulan', filter=Q(sppsiswa__lunas=False))).order_by('-spp__id')
    template_path = 'data/pdf_template.html'
    context = {'laporan': lapor}
    # Buat objek tanggapan Django, dan tentukan content_type sebagai pdf
    response = HttpResponse(content_type='application/pdf')
    # jika langsung mau di download
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # Jika pdf mau ditampilkan attachment dihapus
    response['Content-Disposition'] = 'filename="report.pdf"'
    # temukan template dan render.
    template = get_template(template_path)
    html = template.render(context)

    # buat pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # jika error tampil sebagai dibawah
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@tolakhalaman_ini
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        cocokan = authenticate(request, username=username, password=password)
        if cocokan is not None:
            login(request, cocokan)
            return redirect('home')
        else:
            messages.success(request, 'Username/Password Salah')
    context = {
        'judul': 'Halaman Login',
        'menu': 'login',
    }
    return render(request, 'data/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@pilihan_login
@ijinkan_pengguna(yang_diizinkan=['admin'])
def homePage(request):
    siswa = Siswa.objects.all()
    kelas = Kelas.objects.all()
    total_siswa = siswa.count()
    total_kelas = kelas.count()    
    sppsiswa = SppItem.objects.all().aggregate(Sum('spp__spp'))
    bulan = SppItem.objects.values('spp__bulan').annotate(sppsiswa__lunas_count=Count('spp__bulan', filter=Q(sppsiswa__lunas=True)),not_sppsiswa__lunas_count=Count('spp__bulan', filter=Q(sppsiswa__lunas=False))).order_by('-spp__id')
    jumlah = SppItem.objects.values('spp__spp').annotate(sppsiswa__lunas_count=Sum('spp__spp', filter=Q(sppsiswa__lunas=True)), not_sppsiswa__lunas_count=Sum('spp__spp', filter=Q(sppsiswa__lunas=False)))
    jumlah1 = SppItem.objects.values('spp__bulan').annotate(sppsiswa__lunas_count=Sum('spp__spp', filter=Q(sppsiswa__lunas=True)), not_sppsiswa__lunas_count=Sum('spp__spp', filter=Q(sppsiswa__lunas=False)))
    # dataset = Passenger.objects \
    #     .values('ticket_class') \
    #     .annotate(survived_count=Count('ticket_class', filter=Q(survived=True)),
    #               not_survived_count=Count('ticket_class', filter=Q(survived=False))) \
    #     .order_by('ticket_class')
    # spp = Sppsiswa.objects.get(lunas=True)
    # items = spp.sppitem_set.all().aggregate(Sum('spp__spp'))
    # bulan = SppItem.objects.filter(sppsiswa__lunas=True)
    context = {
        'judul': 'Halaman Beranda',
        'total_siswa': total_siswa,
        'total_kelas': total_kelas,
        'sppsiswa': sppsiswa,
        'bulan': bulan,
        'jumlah': jumlah,
        'jumlah1': jumlah1
        # 'items': items,
    }
    return render(request, 'data/dashboard.html', context)


@login_required(login_url='login')
def siswapage(request):

    if request.user.is_authenticated:
        siswa = request.user.siswa
        sppsiswa, created = Sppsiswa.objects.get_or_create(
            siswa=siswa, lunas=False)
        items = sppsiswa.sppitem_set.all()
        cartItems = sppsiswa.get_cart_item
    else:
        items = []
        sppsiswa = {'get_cart_total': 0}
        cartItems = sppsiswa['get_cart_item']
    siswa = request.user.siswa.namakls
    spp = Spp.objects.filter(kelas=siswa)
    context = {
        'judul': 'Halaman Siswa',
        'items': items,
        'spp': spp,
        'cartItems': cartItems
    }
    return render(request, 'data/siswa_page.html', context)


@login_required(login_url='login')
def cart(request):

    if request.user.is_authenticated:
        siswa = request.user.siswa
        sppsiswa, created = Sppsiswa.objects.get_or_create(siswa=siswa, lunas=False)
        items = sppsiswa.sppitem_set.all()
        cartItems = sppsiswa.get_cart_item
    else:
        items = []
        sppsiswa = {'get_cart_total':0}
        cartItems = sppsiswa['get_cart_item']
    context = {
        'judul': 'Halaman Keranjang',
        'items': items,
        'sppsiswa': sppsiswa,
        'cartItems': cartItems
    }
    return render(request, 'data/cart.html', context)


@login_required(login_url='login')
def checkout(request):

    if request.user.is_authenticated:
        siswa = request.user.siswa
        sppsiswa, created = Sppsiswa.objects.get_or_create(siswa=siswa, lunas=False)
        items = sppsiswa.sppitem_set.all()
        cartItems = sppsiswa.get_cart_item
    else:
        items = []
        sppsiswa = {'get_cart_total': 0}
        cartItems = sppsiswa['get_cart_item']
    context = {
        'judul': 'Halaman CheckOut',
        'items': items,
        'sppsiswa': sppsiswa,
        'cartItems': cartItems
        }
    return render(request, 'data/checkout.html', context)


@login_required(login_url='login')
def updateItem(request):
    data = json.loads(request.body)
    sppId = data['sppId']
    action = data['action']

    print('Action:', action)
    print('spp:', sppId)

    siswa = request.user.siswa
    spp = Spp.objects.get(id=sppId)
    sppsiswa, created = Sppsiswa.objects.get_or_create(siswa=siswa, lunas=False)

    sppItem, created = SppItem.objects.get_or_create(sppsiswa=sppsiswa, spp=spp)
    
    if action == 'add':
        sppItem.quantity = (1)
    elif action == 'remove':
        sppItem.quantity = (sppItem.quantity - 1)

    sppItem.save()

    if sppItem.quantity <= 0:
        sppItem.delete()

    return JsonResponse('Item ditambahkan', safe=False)


# @login_required(login_url='login')
# def updateItema(request, pk):
#     data = json.loads(request.body)
#     sppId = data['sppId']
#     action = data['action']

#     print('Action:', action)
#     print('spp:', sppId)

#     siswa = Siswa.objects.get(nisn=pk)
#     spp = Spp.objects.get(id=sppId)
#     sppsiswa, created = Sppsiswa.objects.get_or_create(siswa=siswa, lunas=True)

#     sppItem, created = SppItem.objects.get_or_create(sppsiswa=sppsiswa, spp=spp)

#     if action == 'add':
#         sppItem.quantity = (1)
#     elif action == 'remove':
#         sppItem.quantity = (sppItem.quantity - 1)

#     sppItem.save()

#     if sppItem.quantity <= 0:
#         sppItem.delete()

#     return JsonResponse('Item ditambahkan', safe=False)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin'])
def laporspp(request):
    items = SppItem.objects.all()
    
    context = {
        'judul': 'Laporan SPP',
        'items': items
    }
    return render(request, 'data/lap_spp.html', context)


@login_required(login_url='login')
def laporsppsis(request):
    if request.user.is_authenticated:
        siswa = request.user.siswa
        sppsiswa, created = Sppsiswa.objects.get_or_create(
            siswa=siswa, lunas=False)
        items = sppsiswa.sppitem_set.all()
        cartItems = sppsiswa.get_cart_item
    else:
        items = []
        sppsiswa = {'get_cart_total': 0}
        cartItems = sppsiswa['get_cart_item']
    siswa = request.user.siswa
    sppsiswa = Sppsiswa.objects.get(siswa=siswa, lunas=True)
    items1 = sppsiswa.sppitem_set.all()
    # items = SppItem.objects.all()
    context = {
        'judul': 'Halaman Laporan SPP Siswa',
        'items1': items1,
        'items': items,
        'cartItems': cartItems
    }
    return render(request, 'data/laporanspp.html', context)
# def statusbayar(request):
#     siswa = request.user.siswa_page
#     sppsiswa, created = Sppsiswa.objects.get_or_create(siswa=siswa, lunas=True)
#     items = sppsiswa.sppitem_set.all()
#     context = {
#         'items': items,
#         'sppsiswa': sppsiswa
#     }
#     return render(request, 'data/status.html', context)


@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin'])
def siswa(request):
    list_siswa = Siswa.objects.all()
    myFilter = SiswaFilter(request.GET, queryset=list_siswa)
    list_siswa = myFilter.qs
    halaman_tampil = Paginator(list_siswa, 2)
    halaman_url = request.GET.get('halaman', 1)
    halaman_siswa = halaman_tampil.get_page(halaman_url)
    if halaman_siswa.has_previous():
        url_previous = f'?halaman={halaman_siswa.previous_page_number()}'
    else:
        url_previous = ''
    if halaman_siswa.has_next():
        url_next = f'?halaman={halaman_siswa.next_page_number()}'
    else:
        url_next = ''
    context = {
        'judul': 'Halaman Siswa',
        'Siswa': list_siswa,
        'myFilter': myFilter,
        'halaman_siswa': halaman_siswa,
        'previous': url_previous,
        'next': url_next
    }
    return render(request, 'data/siswa.html', context)


@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin'])
def Tsiswa(request):
    formregister = SisForm()
    if request.method == 'POST':
        formregister = SisForm(request.POST)
        if formregister.is_valid():
            group_custumer = formregister.save()
            grup = Group.objects.get(name='siswa')
            group_custumer.groups.add(grup)
            Siswa.objects.create(
                user=group_custumer,
                nisn=group_custumer.first_name),
            return redirect('/siswa')
    context = {
        'judul': 'Form Siswa',
        'form': formregister,
    }
    return render(request, 'data/siswa_form.html', context)


@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin'])
def Usiswa(request, pk):
    siswa = Siswa.objects.get(nisn=pk)
    formsiswa = SiswaForm(instance=siswa)
    if request.method == 'POST':
        formedit = SiswaForm(request.POST, instance=siswa)
        if formedit.is_valid:
            formedit.save()
            return redirect('/siswa')
    context = {
        'judul': 'Halaman Edit Siswa',
        'form': formsiswa
    }
    return render(request, 'data/siswa_form.html', context)
    

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin'])
def Hsiswa(request, pk):
    hapussiswa = Siswa.objects.get(nisn=pk)
    hapussiswa.delete()

    return redirect('siswa')


@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin'])
def kelas(request):
    kelas = Kelas.objects.all()
    context = {
        'judul': 'Halaman Kelas',
        'Kelas': kelas
    }
    return render(request, 'data/kelas.html', context)


@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin'])
def Tkelas(request):
    formkelas = KelasForm()
    if request.method == 'POST':
        formkelas = KelasForm(request.POST)
        if formkelas.is_valid:
            formkelas.save()
            return redirect('kelas')
    context = {
        'judul': 'Form Siswa',
        'form': formkelas
    }
    return render(request, 'data/siswa_form.html', context)


@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin'])
def Ukelas(request, pk):
    kelas = Kelas.objects.get(id=pk)
    formkelas = KelasForm(instance=kelas)
    if request.method == 'POST':
        formedit = KelasForm(request.POST, instance=kelas)
        if formedit.is_valid:
            formedit.save()
            return redirect('/kelas')
    context = {
        'judul': 'Halaman Edit Kelas',
        'form': formkelas
    }
    return render(request, 'data/siswa_form.html', context)


@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin'])
def Hkelas(request, pk):
    hapuskelas = Kelas.objects.get(id=pk)
    hapuskelas.delete()

    return redirect('kelas')


@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin'])
def kelassiswa(request):
    kelas = Siswa.objects.values('namakls__id','namakls__namakls').annotate(siswa_count=Count('nama'))
    # kelas = Kelas.objects.all()
    context = {
        'judul': 'Halaman Kelas Siswa',
        'Kelas': kelas
    }
    return render(request, 'data/kelassiswa.html', context)


@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin'])
def Kelas_Siswa(request, pk):
    list_kelas = Kelas.objects.get(id=pk)
    siswa_kelas = list_kelas.siswa_set.all()
    total_siswakelas = siswa_kelas.count()
    context = {
        'judul': 'Halaman Kelas Siswa',
        'kelas': list_kelas,
        'siswa': siswa_kelas,
        'total_siswa': total_siswakelas
    }
    return render(request, 'data/kelassiswa1.html', context)


@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin'])
def spp(request):
    spp = Spp.objects.all()
    halaman_tampil = Paginator(spp, 6)
    halaman_url = request.GET.get('halaman', 1)
    halaman_spp = halaman_tampil.get_page(halaman_url)
    if halaman_spp.has_previous():
        url_previous = f'?halaman={halaman_spp.previous_page_number()}'
    else:
        url_previous = ''
    if halaman_spp.has_next():
        url_next = f'?halaman={halaman_spp.next_page_number()}'
    else:
        url_next = ''
    context = {
        'judul': 'Halaman SPP Siswa',
        'Spp': spp,
        'halaman_spp': halaman_spp,
        'previous': url_previous,
        'next': url_next
    }
    return render(request, 'data/spp.html', context)


@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin'])
def Tspp(request):
    formspp = SppForm()
    if request.method == 'POST':
        formspp = SppForm(request.POST)
        if formspp.is_valid:
            formspp.save()
            return redirect('kelas')
    context = {
        'judul': 'Form Tambah SPP',
        'form': formspp
    }
    return render(request, 'data/siswa_form.html', context)


@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin'])
def Uspp(request, pk):
    spp = Spp.objects.get(id=pk)
    formspp = SppForm(instance=spp)
    if request.method == 'POST':
        formedit = SppForm(request.POST, instance=spp)
        if formedit.is_valid:
            formedit.save()
            return redirect('/spp')
    context = {
        'judul': 'Halaman Edit SPP',
        'form': formspp
    }
    return render(request, 'data/siswa_form.html', context)


@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin'])
def Hspp(request, pk):
    hapusspp = Spp.objects.get(id=pk)
    hapusspp.delete()

    return redirect('spp')


@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin'])
def SPPsiswa(request):
    sppsiswa = Sppsiswa.objects.all()
    myFilter = SPPSiswaFilter(request.GET, queryset=sppsiswa)
    sppsiswa = myFilter.qs
    context = {
        'judul': 'Halaman Request Pembayaran',
        'Sppsiswa': sppsiswa,
        'MyFilter': myFilter
    }
    return render(request, 'data/sppsiswa.html', context)


@login_required(login_url='login')
# @ijinkan_pengguna(yang_diizinkan=['admin'])
def SPPsis(request):
    if request.user.is_authenticated:
        siswa = request.user.siswa
        sppsiswa, created = Sppsiswa.objects.get_or_create(
            siswa=siswa, lunas=False)
        items = sppsiswa.sppitem_set.all()
        cartItems = sppsiswa.get_cart_item
    else:
        items = []
        sppsiswa = {'get_cart_total': 0}
        cartItems = sppsiswa['get_cart_item']
    siswa = request.user.siswa
    sppsiswa = siswa.sppsiswa_set.all()
    sppitem = SppItem.objects.filter(sppsiswa=sppsiswa)
    context = {
        'judul': 'Halaman Request Pembayaran',
        'Sppsiswa': sppsiswa,
        'item': sppitem,
        'items': items,
        'spp': spp,
        'cartItems': cartItems
    }
    return render(request, 'data/sppsis.html', context)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin'])
def TSPPsiswa(request):
    formspp = SppSiswaForm()
    if request.method == 'POST':
        formspp = SppSiswaForm(request.POST)
        if formspp.is_valid:
            formspp.save()
            return redirect('sppsiswa')
    context = {
        'judul': 'Form Tambah SPP Siswa',
        'form': formspp
    }
    return render(request, 'data/siswa_form.html', context)


@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin'])
def USPPsiswa(request, pk):
    spp = Sppsiswa.objects.get(id=pk)
    formspp = SppSiswaForm(instance=spp)
    if request.method == 'POST':
        formedit = SppSiswaForm(request.POST, instance=spp)
        if formedit.is_valid:
            formedit.save()
            return redirect('/sppsiswa')
    context = {
        'judul': 'Halaman Edit SPP Siswa',
        'form': formspp
    }
    return render(request, 'data/siswa_form.html', context)


@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin'])
def HSPPsiswa(request, pk):
    hapusspp = Sppsiswa.objects.get(id=pk)
    hapusspp.delete()

    return redirect('sppsiswa')


@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin'])
def sppitem(request):
    items = SppItem.objects.all()
    context = {
        'judul': 'Halaman SPP Siswa',
        'Spp': items
    }
    return render(request, 'data/sppitem.html', context)


@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin'])
def Tsppitem(request):
    formspp = SPPitemForm()
    if request.method == 'POST':
        formspp = SPPitemForm(request.POST)
        if formspp.is_valid:
            formspp.save()
            return redirect('kelas')
    context = {
        'judul': 'Form Tambah SPP',
        'form': formspp
    }
    return render(request, 'data/siswa_form.html', context)


@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin'])
def Usppitem(request, pk):
    spp = SppItem.objects.get(id=pk)
    formspp = SPPitemForm(instance=spp)
    if request.method == 'POST':
        formedit = SPPitemForm(request.POST, instance=spp)
        if formedit.is_valid:
            formedit.save()
            return redirect('/spp')
    context = {
        'judul': 'Halaman Edit SPP',
        'form': formspp
    }
    return render(request, 'data/siswa_form.html', context)


@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin'])
def Hsppitem(request, pk):
    hapusspp = SppItem.objects.get(id=pk)
    hapusspp.delete()

    return redirect('sppitem')

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin'])
def petugas(request):
    petugas = Bendahara.objects.all()

    context = {
        'judul': 'Halaman Petugas',
        'petugas': petugas
    }
    return render(request, 'data/petugas.html', context)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin'])
def Tpetugas(request):
    formpetugas = PetugasForm()
    if request.method == 'POST':
        formsimpan = PetugasForm(request.POST)
        if formsimpan.is_valid:
            petugas = formsimpan.save()
            Bendahara.objects.create(
                user=petugas,
                namapetugas=petugas.first_name),
            return redirect('/petugas')

    context = {
        'judul': 'Halaman Petugas',
        'form': formpetugas
    }
    return render(request, 'data/siswa_form.html', context)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin'])
def Upetugas(request, pk):
    petugas = Bendahara.objects.get(id=pk)
    formpetugas = UPetugasForm(instance=petugas)
    if request.method == 'POST':
        formedit = UPetugasForm(request.POST, instance=petugas)
        if formedit.is_valid:
            formedit.save()
            return redirect('/petugas')
    context = {
        'judul': 'Halaman Edit Petugas',
        'form': formpetugas
    }
    return render(request, 'data/siswa_form.html', context)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin'])
def Hpetugas(request, pk):
    hapuspetugas = Bendahara.objects.get(id=pk)
    hapuspetugas.delete()

    return redirect('petugas')