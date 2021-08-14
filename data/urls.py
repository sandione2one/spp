from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),

    path('', views.homePage, name="home"),
    path('siswa/', views.siswa, name="siswa"),
    path('tambah_siswa/', views.Tsiswa, name="tambah_siswa"),
    path('ubah_siswa/<str:pk>', views.Usiswa, name="ubah_siswa"),
    path('hapus_siswa/<str:pk>', views.Hsiswa, name="hapus_siswa"),

    path('kelas/', views.kelas, name="kelas"),
    path('tambah_kelas/', views.Tkelas, name="tambah_kelas"),
    path('ubah_kelas/<str:pk>', views.Ukelas, name="ubah_kelas"),
    path('hapus_kelas/<str:pk>', views.Hkelas, name="hapus_kelas"),

    path('spp/', views.spp, name="spp"),
    path('tambah_spp/', views.Tspp, name="tambah_spp"),
    path('ubah_spp/<str:pk>', views.Uspp, name="ubah_spp"),
    path('hapus_spp/<str:pk>', views.Hspp, name="hapus_spp"),

    path('tambah_sppsiswa/', views.TSPPsiswa, name="tambah_sppsiswa"),
    path('sppsiswa/', views.SPPsiswa, name="sppsiswa"),
    path('ubah_sppsiswa/<str:pk>', views.USPPsiswa, name="ubah_sppsiswa"),
    path('hapus_sppsiswa/<str:pk>', views.HSPPsiswa, name="hapus_sppsiswa"),
    path('laporsppsiswa/', views.laporspp, name="laporsppsiswa"),

    path('sppitem/', views.sppitem, name="sppitem"),
    path('tambah_sppitem/', views.Tsppitem, name="tambah_sppitem"),
    path('ubah_sppitem/<str:pk>', views.Usppitem, name="ubah_sppitem"),
    path('hapus_sppitem/<str:pk>', views.Hsppitem, name="hapus_sppitem"),
    # path('update_itema/', views.updateItema, name="update_itema"),

    path('kelassiswa/', views.kelassiswa, name="kelassiswa"),
    path('kelas_siswa/<str:pk>', views.Kelas_Siswa, name='kelas_siswa'),


    path('siswapage/', views.siswapage, name="siswapage"),
    path('sppsis/', views.SPPsis, name="sppsis"),
    path('laporsppsis/', views.laporsppsis, name="laporsppsis"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),

    path('cetak/', views.pdflap, name="cetak"),
    # path('pdf_view/', views.ViewPDF.as_view(), name="pdf_view"),
    # path('pdf_download/', views.DownloadPDF.as_view(), name="pdf_download"),

    
    path('petugas/', views.petugas, name="petugas"),
    path('Tpetugas/', views.Tpetugas, name="Tpetugas"),
    path('Upetugas/<str:pk>', views.Upetugas, name="Upetugas"),
    path('Hpetugas/<str:pk>', views.Hpetugas, name="Hpetugas"),

]
