Link Adaptable:
https://gameartifactinventory.adaptable.app/main/

# Proses implementasi checklist tugas

## Membuat proyek Django baru
Pertama saya membuat direktori baru game_inventory dan di dalam direktori itu saya membuat virtual environment dengan menjalankan
```
python -m venv env
```
lalu saya mengaktifkan virtual environment dengan menjalankan
```
env\Scripts\activate.bat
```
Lalu saya membuat requirements.txt yang berisi beberapa dependencies yang dibutuhkan untuk membuat proyek Django. Isi dari requirements.txt adalah
```
django
gunicorn
whitenoise
psycopg2-binary
requests
urllib3
```
Lalu saya menginstal semua dependencies dengan perintah
```
pip install -r requirements.txt
```
Semua dependencies yang diperlukan sudah diinstal. Selanjutnya saya membuat proyek Django baru dengan
```
django-admin startproject game_inventory .
```
Untuk deployment nanti, pada settings.py pada folder game_inventory ditambahkan "*" pada ALLOWED_HOST untuk mengizinkan semua host untuk mengakses aplikasi.

## Membuat aplikasi main pada proyek yang sudah dibuat
Sekarang dibuat aplikasi baru bernama main dengan menjalankan perintah berikut di command prompt
```
python manage.py startapp main
```
Selanjutnya saya pertama mendaftarkan aplikasi main pada proyek game_inventory. Pada direktori game_inventory, pada file settings.py ditambahkan 'main' pada INSTALLED_APPS menjadi
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
]
```

## Membuat model pada aplikasi main dengan nama Item
Selanjutnya pada direktori game_inventory\main pada models.py dibuat menjadi
```
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    description = models.TextField()
```
sesuai deskripsi tugas.
Lalu dilakukan migrasi dengan
```
python manage.py makemigrations
python manage.py migrate
```
untuk mencatat perubahan model pada basis data.

## Membuat sebuah fungsi pada views.py untuk dikembalikan ke dalam sebuah template HTML
Sebelumnya dibuat folder baru untuk templates html pada main bernama templates dan di dalamnya dibuat file main.html berisi berikut
```
<html>
<head>
    <title>Game Inventory</title>
</head>
<body>
    <h1>Artifact Game Inventory (inspired by CK2 Tianxia MOD)</h1>
    <p>{{ nama }}</p>
    <p>{{ kelas }}</p>
	<h5> Item Name : <em>{{ name }}</em> </h5>
	<h5> Amount : {{ amount }} </h5>
	<h5> Description : {{ description }} </h5>
</body>
</html>
```
Selanjutnya pada direktori main, pada file views.py diedit sesuai dengan context pada file template main.html dengan membuat fungsi show_main. views.py menambahkan data yang dimau untuk dirender bersama template html sebelum diberikan ke user.
```
def show_main(request):
    context = {
        # data untuk ditambahkan ke main.html
    }

    return render(request, "main.html", context)
```

## Membuat sebuah routing pada urls.py aplikasi main untuk memetakan fungsi yang telah dibuat pada views.py
Membuat file baru urls.py di aplikasi main dengan isi berikut
```
from django.urls import path
from main.views import show_main

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
]
```
Berguna sebagai pengarah rute saat aplikasi main diakses. Kode di atas membuat show_main dari views.py dilakukan saat url dengan path di atas diakses.

## Melakukan routing pada proyek agar dapat menjalankan aplikasi main
Pada urls.py pada direktori proyek game_inventory, isi urls.py menjadi
```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include('main.urls')),
]
```
Mengimpor include untuk dapat mengambil path URL dari aplikasi lain (main). Path main/ saat diakses akan menuju path yang ada di dalam main.urls.

## Bonus : Testing
Untuk testing, dilakukan testing berjalannya url di aplikasi dan kesesuaian template sesuai tutorial. Selain itu juga ada testing kesesuaian detail model item yang dibuat.
Dibuat contoh mode item pada testcase lalu dicocokkan detail dari item yang dibuat dengan yang seharusnya.
Untuk detail dapat dilihat di [sini](main/tests.py)

# Bagan request Client ke aplikasi Django dan responnya


# Alasan penggunaan virtual environment dan apa yang terjadi jika tidak menggunakan virtual environment
Penggunaan virtual environment bertujuan untuk membatasi proyek dari global environment python. Jika kita membuat banyak proyek dengan berbagai dependensi yang berbeda, maka lebih efektif membuat virtual environment untuk setiap proyek yang ada. Dengan terpisahnya dependensi antar proyek, maka developer dapat bekerja dengan python dan package yang versinya berbeda-beda sesuai kebutuhan proyek.
Jika tidak menggunakan virtual environment, kita tetap dapat membuat proyek Django. Namun terdapat risiko konflik dependensi antar proyek dan konflik versi package.

# MVC, MVT, MVVM dan perbedaan dari ketiganya