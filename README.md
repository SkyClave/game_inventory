[Link Aplikasi](http://alwin-djuliansah-tugas.pbp.cs.ui.ac.id)

# Tugas 6

## Proses implementasi checklist Tugas

### AJAX Get (Pada daftar item)

#### Ubahlah kode cards data item agar dapat mendukung AJAX GET

Pertama dibuat fungsi untuk mendapatkan data item dalam bentuk json untuk AJAX nanti di views.py seperti ini:
```
def get_item_json(request):
    artifact_item = Item.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize('json', artifact_item))
```
Fungsi ini lalu diimport lalu dirouting di urls.py. Sekarang ada fungsi yang mengembalikan data item dalam json untuk AJAX get.

#### Lakukan pengambilan task menggunakan AJAX GET

Lalu pada main.html loop data item diubah menjadi kosong. Data-data yang mau diupdate diberi id html tagnya. Lalu dibuat script di bawah kode html sebagai berikut.
```
	async function getItem() {
        return fetch("{% url 'main:get_item_json' %}").then((res) => res.json())
    }
	async function refreshItem() {
        document.getElementById("daftar_item").innerHTML = ""
		document.getElementById("counter_item").innerHTML = ""
		document.getElementById("counter_total").innerHTML = ""
        const items = await getItem()
        let htmlString = ``
		let count = 0
		let sum = 0
        items.forEach((item) => {
            htmlString += `<div class="col-lg-4 mb-4">
				<div class="card" ${index == items.length - 1 ? 'style="color: gold;"' : ''}>
					<div class="card-body">
						<h3 class="card-title">${item.fields.name}<h3>
						<p class="card-text">Amount : ${item.fields.amount}</p>
						<p class="card-text">Description : ${item.fields.description}</p>
					</div>
					<div class="btn-group">
						<a class="btn btn-primary" onclick="addOneItem(${item.pk})">+</a>
						<a class="btn btn-primary" onclick="decreaseItem(${item.pk})">-</a>
						<a class="btn btn-danger" onclick="deleteItem(${item.pk})">Remove</a>
					</div>
				</div>
			</div>`
			count += 1
			sum += item.fields.amount
        })
        
        document.getElementById("daftar_item").innerHTML = htmlString
		document.getElementById("counter_item").innerHTML = `Ada ${count} jenis item dalam inventory`
		document.getElementById("counter_total").innerHTML = `Ada total ${sum} item dalam inventory`
    }

    refreshItem()
```
Fungsi getItem akan mendapatkan data item dalam json. Lalu fungsi refreshItem akan mengubah data isi html berdasarkan data item terbaru yang diambil dari getItem tanpa perlu reload. Fungsi refreshItem juga menghitung kembali jumlah jenis dan total item yang ada dan mengupdate jumlahnya di data isi html tanpa perlu reload.

### AJAX POST (menambahkan item dan update tanpa reload)

#### Buatlah sebuah tombol yang membuka sebuah modal dengan form untuk menambahkan item.

Implementasi dengan menambahkan tombol ke navbar yang sudah ada.
```
<li class="nav-item">
	<a class="nav-link" data-bs-toggle="modal" data-bs-target="#exampleModal">Add Artifact by AJAX</a>
</li>
```
Untuk implementasi modal, kodenya mengikuti tutorial seperti ini.
```
<div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
	<div class="modal-dialog">
		<div class="modal-content">
			<div class="modal-header">
				<h1 class="modal-title fs-5" id="exampleModalLabel">Add New Product</h1>
				<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
			</div>
			<div class="modal-body">
				<form id="form" onsubmit="return false;">
					{% csrf_token %}
					<div class="mb-3">
						<label for="name" class="col-form-label">Name:</label>
						<input type="text" class="form-control" id="name" name="name"></input>
					</div>
					<div class="mb-3">
						<label for="amount" class="col-form-label">Amount:</label>
						<input type="number" class="form-control" id="amount" name="amount"></input>
					</div>
					<div class="mb-3">
						<label for="description" class="col-form-label">Description:</label>
						<textarea class="form-control" id="description" name="description"></textarea>
					</div>
				</form>
			</div>
			<div class="modal-footer">
				<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
				<button type="button" class="btn btn-primary" id="button_add" data-bs-dismiss="modal">Add Product</button>
			</div>
		</div>
	</div>
</div>
```

#### Buatlah fungsi view baru untuk menambahkan item baru ke dalam basis data.

Dibuat fungsi yang menerima request jika request post mengambil data item yang mau ditambahkan, membuat item dengan data yang diberikan, lalu mengembalikan response HTML 201 Created.
```
@csrf_exempt
def add_item_ajax(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        amount = request.POST.get("amount")
        description = request.POST.get("description")
        user = request.user

        new_item = Item(name=name, amount=amount, description=description, user=user)
        new_item.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()
```

#### Buatlah path /create-ajax/ yang mengarah ke fungsi view yang baru kamu buat.

Di urls.py diimpor fungsi dari views.py lalu ditambahkan routing di urls.py seperi ini.
```
urlpatterns = [
	...
	path('create-ajax/', add_item_ajax, name='add_item_ajax'),
]
```

#### Hubungkan form yang telah kamu buat di dalam modal kamu ke path /create-ajax/ dan lakukan refresh pada halaman utama secara asinkronus untuk menampilkan daftar item terbaru tanpa reload halaman utama secara keseluruhan.

Pertama dibuat fungsi script di main.html yang menghandle penambahan item seperti ini
```
	function addItem() {
        fetch("{% url 'main:add_item_ajax' %}", {
            method: "POST",
            body: new FormData(document.querySelector('#form'))
        }).then(refreshItem)

        document.getElementById("form").reset()
        return false
    }
```
Fungsi ini mempost data dari form untuk membuat item baru ke database lalu mengupdate kembali isi html dengan data yang terbaru dari database (update memanfaatkan fungsi refresh item yang dibuat sebelumnya). Lalu isi form direset.

Lalu button pada form (modal) yang dibuat dihubungkan dengan fungsi di atas seperti ini.
```
document.getElementById("button_add").onclick = addItem
```
Sekarang item baru yang ditambahkan akan langsung terlihat pada halaman data item tanpa perlu reload.

### Melakukan perintah collectstatic

Pada settings.py di directory game_inventory ditambahkan kode ini di bawah STATIC_URL dan import os
```
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
```
Lalu dijalankan perintah berikut di command line root directory.
```
python manage.py collectstatic
```
Sekarang file static pada aplikasi sudah ada di folder static pada root directory.

### Implementasi Bonus : Menambahkan fungsionalitas hapus dengan menggunakan AJAX DELETE

Ditambahkan fungsi berikut di script main.html:
```
	function deleteItem(itemId) {
		fetch(("/remove_item/" + itemId), {
            method: "DELETE"
        }).then(refreshItem)
		return false
	}
	
	function addOneItem(itemId) {
		fetch(("/add_item/" + itemId), {
            method: "GET"
        }).then(refreshItem)
		return false
	}
	
	function decreaseItem(itemId) {
		fetch(("/decrease_item/" + itemId), {
            method: "GET"
        }).then(refreshItem)
		return false
	}
```
Fungsi yang dibuat memanfaatkan fungsi yang sudah dibuat pada week sebelumnya. 3 fungsi di views.py diubah menjadi tidak kembali (redirect) ke main melainkan return httpresponse dengan status code yang sesuai dengan request yang dibuat. Untuk update data isi html menggunakan fungsi refresh item yang dibuat sebelumnya.

## Pertanyaan

### Jelaskan perbedaan antara asynchronous programming dengan synchronous programming.

Synchronous programming menjalankan programnya satu per satu dan program lain belum bisa berjalan jika program sebelumnya belum selesai sedangkan asynchronous programming dapat menjalankan programnya secara bersamaan karena tidak perlu menunggu program sebelumnya selesai. Pada web, asynchronous programming mengacu pada banyak request yang dapat dilakukan secara bersamaan tanpa perlu menunggu response sedangkan synchronous harus menunggu response dari server untuk melakukan request berikutnya.

### Dalam penerapan JavaScript dan AJAX, terdapat penerapan paradigma event-driven programming. Jelaskan maksud dari paradigma tersebut dan sebutkan salah satu contoh penerapannya pada tugas ini.

Paradigma event-driven programming adalah paradigma programming di mana alur eksekusi program bergantung terhadap pemicu atau event. Event bisa berasal dari pengguna yang melakukan klik mouse, keyboard, atau alat lainnya. Contoh penerapan paradigma event-driven programming pada tugas ini adalah saat menghubungkan button submit form modal dengan fungsi yang menyimpan data item ke database.
```
document.getElementById("button_add").onclick = addItem
```
Ketika ada event dari pengguna yaitu klik button dengan id button_add, maka program akan mengeksekusi fungsi addItem untuk menambahkan data item baru ke database.

### Jelaskan penerapan asynchronous programming pada AJAX.

Penerapan asynchronous programming pada AJAX adalah dengan menerapkan ketika ada request, kita tidak perlu mereload halamn web. AJAX menggunakan async dan await untuk asynchronous programming. Async menandakan bahwa suatu fungsi menjalankan operasi asynchronous dan await menunda eksekusi hingga operasi asynchronous selesai dan memberikan response.

### Pada PBP kali ini, penerapan AJAX dilakukan dengan menggunakan Fetch API daripada library jQuery. Bandingkanlah kedua teknologi tersebut dan tuliskan pendapat kamu teknologi manakah yang lebih baik untuk digunakan.

Fetch API adalah API built-in dari JavaScript yang lebih modern, ringan, dan modular jika dibandingkan dengan jQuery. jQuery adalah library JavaScript yang lebih lengkap dan memiliki abstraksi yang lebih baik namun berukuran sangat besar jika dibandingkan dengan Fetch API.

Menurut saya, jika hanya menggunakan AJAX saja seperti tugas PBP ini, sebaiknya menggunakan Fetch API karena lebih ringan dan sesuai kebutuhan dibandingkan menggunakan jQuery yang mungkin banyak fiturnya tidak diperlukan dalam proyek yang dibuat.

# Tugas 5

## Proses implementasi checklist Tugas

### Kustomisasi desain pada templat HTML yang telah dibuat pada Tugas 4 dengan menggunakan CSS atau CSS framework

Untuk kustomisasi desain html, digunakan Bootstrap. Pertama ditambahkan bootstrap ke aplikasi dengan memasukkannya di template base.html di root. Ditambahkan script dalam [link ini](https://getbootstrap.com/docs/5.3/getting-started/introduction/).

``` <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous"> ```

pada head 

```<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>```

pada body

base.html juga diubah menjadi color theme dark.

### Kustomisasi halaman login, register, dan tambah inventori semenarik mungkin

Halaman login, register, dan tambah inventori diubah menjadi approach card dengan title halaman sebagai card header dan form login/register/tambah inventori sebagai card body.

Contoh seperti pada halaman register, cardnya seperti ini:

```
<div class="card">
	<div class="card-header">
		<h1 class="text-left">Register</h1>
	</div>
    <div class="card-body">
		<main class="form-signin w-100 m-auto">
			<form method="POST" >  
				{% csrf_token %}  
				<table class="table">
					{{ form.as_table }}  
					<tr>  
						<td></td>
						<td>
							<div class="text-left">
								<button class="btn btn-primary" type="submit">Daftar</button>
							</div>
						</td>  
					</tr>  
				</table>  
			</form>
		</main>
		{% if messages %}
			<div class="alert alert-danger mt-3">
				<ul>   
					{% for message in messages %}  
						<li>{{ message }}</li>  
						{% endfor %}  
				</ul>
			</div>
		{% endif %}
	</div>
</div>
```
Untuk halaman login formnya dibuat floating form.

### Kustomisasi halaman daftar inventori menjadi lebih berwarna maupun menggunakan apporach lain

Untuk halaman daftar inventori, dibuat dengan approach card juga. Dibuat 2 container, satu buat isi nama dan banyak total dan jenis item. Yang satu lagi untuk meletakkan card item yang akan ditampilkan. Card satu item terdiri atas card title berisi nama item dan card text berisi jumlah dan deskripsi item. Implementasi sebagai berikut:
```
<div class="container mt-5">
	<div class="row">
		{% for item in items %}
		<div class="col-lg-4 mb-4">
			<div class="card">
				<div class="card-body">
					<h3 class="card-title">{{item.name}}<h3>
					<p class="card-text">Amount : {{item.amount}}</p>
					<p class="card-text">Description : {{item.description}}</p>
				</div>
				<div class="btn-group">
					<a href="{% url 'main:add_item' item.id %}" class="btn btn-primary">+</a>
					<a href="{% url 'main:decrease_item' item.id %}" class="btn btn-primary">-</a>
					<a href="{% url 'main:remove_item' item.id %}" class="btn btn-danger">Remove</a>
				</div>
			</div>
		</div>
		{% endfor %}
	</div>
</div>
```
Dibandingkan tugas lalu, tombol logout dan add item di bawah dipindahkan ke atas dan dimasukkan ke navbar bersama nama aplikasi dan username user yang login.

### Implementasi Bonus

Edit card untuk mengecek dalam loop apakah loop terakhir atau bukan. Jika iya tambahkan style warna gold ke text di item terakhir. Dari
```<div class="card">```
menjadi
```<div class="card {% if forloop.last %}" style="color: gold;"{% endif %}">```

## Pertanyaan

### Jelaskan manfaat dari setiap element selector dan kapan waktu yang tepat untuk menggunakannya.
- Element selector, untuk memilih elemen dengan tag tertentu. Ini berguna apabila kita ingin memberikan style yang sama pada elemen yang sama tagnya.
- ID selector, untuk memilih elemen yang tag nya memiliki id tertentu. Karena ID unik untuk setiap elemen. Ini tepat digunakan ketika kita hanya ingin mengubah style dari satu elemen tertentu saja.
- Class selector, untuk memilih elemen dengan class / karakteristik sama. Ini dapat digunakan apabila kita ingin elemen dengan karakteristik yang sama juga mempunyai style yang sama.

### Jelaskan HTML5 Tag yang kamu ketahui.

- ```<nav>``` untuk membuat page navigasi
- ```<audio``` untuk menyisipkan audio dalam web.
- ```<video>``` untuk memasukkan video ke dalam web.
- ```<section>``` untuk mendefinisikan bagian-bagian dari satu halaman web. 

### Jelaskan perbedaan antara margin dan padding.

Padding mengosongkan area di sekitar konten, padding mengatur ada ruang kosong antara border dan konten dalam elemen. Sedangkan margin mengosongkan area di sekitar border. Margin mengatur jarak antara border satu elemen dengan elemen lainnya.

### Jelaskan perbedaan antara framework CSS Tailwind dan Bootstrap. Kapan sebaiknya kita menggunakan Bootstrap daripada Tailwind, dan sebaliknya?

Bootstrap adalah framework CSS yang sudah menyediakan berbagai komponen bawaan seperti navbar, dan lain-lain sehingga dapat langsung digunakan untuk tampilan aplikasi. Sedangkan Tailwind adalah framework CSS yang kita membangun tampilan dari kelas-kelas utilitas yang didefinisikan sebelumnya.

Bootstrap sebaiknya digunakan daripada Tailwind ketika kita perlu membuat proyek dalam waktu cepat dan tidak perlu ada kustomisasi pada proyek yang dibuat. Maka Bootstrap dengan berbagai komponen bawaannya dapat membantu mempercepat pembuatan aplikasi.

Sebaliknya, Tailwind sebaiknya digunakan daripada Bootstrap jika kita membutuhkan kustomisasi yang detail pada aplikasi yang dibuat. Dengan Tailwind, kita dapat membangun tampilan dengan kustomisasi yang dimau dengan kelas-kelas utilitas yang ada.

# Tugas 4

## Proses implementasi checklist tugas

### Mengimplementasikan fungsi registrasi, login, dan logout serta menampilkan data user dan cookie seperti last login

Untuk fungsi register, dimanfaatkan UserCreationForm formulir bawaan dari Django untuk registrasi user. Lalu dibuat template html untuk form register lalu dibuat fungsi register menambahkan UserCreationForm pada template html di views.py main lalu ditambahkan routing di urls.py.

Untuk fungsi login, dibuat form login sendiri dengan membuat langsung di template html form dengan field username dan password. Lalu dibuat fungsi login dengan import authenticate di views.py dan dilakukan routing juga. Untuk menampilkan data user dan last login, ditambahkan pada setiap login dicatat waktu login sebagai cookie, lalu main.html dan show_main diubah context dan variabelnya untuk menampilkan username dan last login.

Selanjutnya dilakukan restriksi halaman main dengan menambahkan ```@login_required(login_url='/login')``` di atas fungsi show_main.

Untuk logout, dibuat tambahan button yang dihubungkan dengan routing logout di urls.py. Lalu dibuat fungsi logout di views.py yang dirouting di urls.py. Saat logout data cookie last login dihapus.

Isi fungsi register, login, dan logout di views.py adalah :
```
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main")) 
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)
    
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response
```

### Menghubungkan model Item dengan User dan membuat dua akun pengguna dengan masing-masing tiga dummy data menggunakan model

Membuat dua user baru dengan akses url register. Lalu pada models.py ditambahkan field user seperti berikut
```
user = models.ForeignKey(User, on_delete=models.CASCADE)
```
Lalu mengubah create_item agar item yang dibuat sesudah perubahan model dilink ke user yang membuatnya dan show_main menambahkan filter agar suatu item hanya dapat dilihat user yang terkait. Selanjutnya melakukan migrasi dan menghubungkan item yang sudah ada sebelum migrasi dengan user yang dibuat. Lalu membuat tiga item masing-masing untuk user yang dibuat.

### Implementasi Bonus : Increment, Decrement, Remove

Didefiniskan fungsi pada views.py sebagai berikut:
```
@login_required(login_url='/login')
def add_item(request, id):
    try:
        data = Item.objects.filter(user=request.user).filter(pk=id).first()
        data.amount += 1
        data.save()
    finally:
        return redirect('/')

@login_required(login_url='/login')
def decrease_item(request, id):
    try:
        data = Item.objects.filter(user=request.user).filter(pk=id).first()
        data.amount -= 1
        if data.amount <= 0:
            data.delete()
            return redirect('/')
        data.save()
    finally:
        return redirect('/')

@login_required(login_url='/login')
def remove_item(request, id):
    try:
        data = Item.objects.filter(user=request.user).filter(pk=id).first()
        data.delete()
    finally:
        return redirect('/')
```
Kode di atas mencari item milik user yang login saat itu dengan parameter id, lalu dilakukan perubahan jumlah item dan disimpan. Jika jumlah item menjadi 0 atau remove option, maka item dihapus dari database. Lalu redirect ke main.

Tiga fungsi ini lalu dirouting di urls.py. Pada main.html ditambahkan 3 button di iterasi setiap tabel sebagai berikut dan dihubungkan ke path yang sudah dibuat.
```
<td><a href="{% url 'main:add_item' item.id %}"><button>+</button></a></td>
<td><a href="{% url 'main:decrease_item' item.id %}"><button>-</button></a></td>
<td><a href="{% url 'main:remove_item' item.id %}"><button>Remove</button></a></td>
```

## Pertanyaan

### Apa itu Django UserCreationForm, dan jelaskan apa kelebihan dan kekurangannya?

UserCreationForm adalah form bawaan Django yang berguna untuk registrasi user baru. UserCreationForm memiliki kelebihan yaitu user yang dibuat langsung disimpan dalam database dan terintegrasi dalam autentikasi Django. Kekurangannya adalah UserCreationForm hanya form registrasi simpel saja. Ketika kita membutuhkan form registrasi yang lebih kompleks, kita harus mengkustomisasinya sendiri meskipun dapat memanfaatkan inheritance dari UserCreationForm.

### Apa perbedaan antara autentikasi dan otorisasi dalam konteks Django, dan mengapa keduanya penting?

Autentikasi adalah proses verifikasi user, dapat menggunakan kredensial seperti username dan password. Contoh seperti login. Sedangkan otorisasi adalah proses verifikasi akses user ke suatu data atau lainnya setelah autentikasi. Keduanya penting karena untuk menjaga keamanan data aplikasi. Autentikasi memastikan user yang mengakses aplikasi adalah user yang sah, sedangkan otorisasi memastikan akses data user terkontrol dengan baik.

### Apa itu cookies dalam konteks aplikasi web, dan bagaimana Django menggunakan cookies untuk mengelola data sesi pengguna?

Cookies adalah sebuah file penyimpanan yang disimpan pada browser oleh aplikasi web saat kita mengakses aplikasi. Cookies bersifat sementara dan dapat menyimpan data seperti data login pengguna. Django menyimpan id sesi user pada cookies. Hal ini membuat Django dapat mengenali user apabila user mengakses url yang sama kembali.

### Apakah penggunaan cookies aman secara default dalam pengembangan web, atau apakah ada risiko potensial yang harus diwaspadai?

Penggunaan cookies rawan karena cookies dapat dilihat langsung oleh user. Berarti cookie dapat dicuri dengan mudah apabila user lengah. Namun cookie dapat dienkripsi sehingga aman. Risiko potensial yang harus diwaspadai adalah cookie hijacking / session hijacking yang mencuri cookie user untuk mendapat unauthorized access.

# Tugas 3

## Proses implementasi checklist tugas

### Persiapan

Sebelumnya virtual environment dijalankan lalu merubah routing main/ menjadi / agar sesuai konvensi yang ada. Lalu membuat base.html dan set sebagai template di root folder dan edit main.html agar menjadikan base.html sebagai template.

### Membuat input form untuk menambahkan objek model pada app sebelumnya

Membuat form yang akan digunakan pada forms.py pada app main (Django sudah menghandle form dengan library django.forms). Kita tinggal membuat ModelForm sesuai objek model Item yang sudah ada. Isi forms.py :
```
from django.forms import ModelForm
from main.models import Item

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ["name", "amount", "description"]
```

Lalu dibuat template html untuk halaman form di folder templates main.
```
{% extends 'base.html' %} 

{% block content %}
<h1>Add New Item</h1>

<form method="POST">
    {% csrf_token %}
    <table>
        {{ form.as_table }}
        <tr>
            <td></td>
            <td>
                <input type="submit" value="Add Item"/>
            </td>
        </tr>
    </table>
</form>

{% endblock %}
```
```form``` pada kode di atas mengacu pada ModelForm. Di views.py nanti, form akan diisi dengan ItemForm yang dibuat dalam fungsi create_item. Sementara itu csrf token adalah token yang digenerate Django untuk fungsi keamanan. Setiap form baru dibuat, token baru akan dibuat/generate. Selanjutnya dibuat fungsi create_item di views.py dengan menambahkan kode ini:
```
def create_item(request):
    form = ItemForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "create_item.html", context)
```
Kode ini berguna saat dipanggil sebagai fungsi yang dieksekusi saat path create-item diakses user merender ItemForm ke template html form yang ada. Lalu pada urls.py (main) ditambahkan path baru pada urlpatterns agar form dapat diakses.
```
path('create-item', create_item, name='create_item')
```
Dengan ini saat user mencoba mengakses path create-item maka create_item.html berisi form untuk menambahkan Item akan dikembalikan sebagai response.

Di file-file yang diedit di atas dilakukan beberapa import tambahan beberapa library. (Library yang diimport sama dengan saat tutorial 2)

### Tambahkan 5 fungsi views untuk melihat objek yang sudah ditambahkan dalam format HTML, XML, JSON, XML by ID, dan JSON by ID

Menambahkan fungsi-fungsi berikut pada views.py :

```
def show_html(request):
    items = Item.objects.all()
    item_counter = items.count()
    item_sum = sum([item.amount for item in items])
    context = {
        'item_counter': item_counter,
        'item_sum': item_sum,
        'items': items,
    }
    return render(request, "show_item.html", context)

def show_xml(request):
    data = Item.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")
    
def show_json(request):
    data = Item.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
    
def show_xml_by_id(request, id):
    data = Item.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")
    
def show_json_by_id(request, id):
    data = Item.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
```

Untuk implementasi tampilan HTML, sama seperti tugas sebelumnya, membuat template html baru, lalu merender data semua item di database ke template html. Untuk XML dan JSON, dimanfaatkan serializers yang akan mengubah (serialisasi) data Item dari database menjadi format XML dan JSON. Data XML dan JSON yang sudah diekstrak lalu dikembalikan dalam bentuk HTTPResponse. Untuk implementasi XML by ID dan JSON by ID (mencari data Item dengan ID tertentu), pertama dicari (filter) data Item dengan ID yang dimau lalu diserialisasi (ubah) menjadi format XML dan JSON lalu dikembalikan sebagai HTTPResponse.

### Membuat routing URL untuk masing-masing views yang telah ditambahkan

Menambahkan urlpatterns pada urls.py (main) dan import semua fungsi yang dibuat di views.py ke urls.py 
```
from django.urls import path
from main.views import show_main, create_item, show_html, show_xml, show_json, show_xml_by_id, show_json_by_id

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-item', create_item, name='create_item'),
    path('html/', show_html, name='show_html'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<int:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'),
]
```
Penambahan path untuk masing-masing views seperti tugas sebelumnya, membuat path yang terhubung dengan fungsi yang ada pada views.py

## Pertanyaan

### Apa perbedaan antara form POST dan form GET dalam Django?

GET adalah method HTTP Request yang mengirimkan request dan data request biasanya berada di url yang diakses. GET adalah method yang sangat simpel dibandingkan dengan POST namun data yang dikirim akan mudah dilihat karena berada di url itu sendiri. POST sendiri adalah method HTTP Request yang mengutamakan pengiriman data. Pada POST, data dikirim berada dalam request itu sendiri sehingga meningkatkan keamanan namun lebih rumit dibandingkan dengan GET.

### Apa perbedaan utama antara XML, JSON, dan HTML dalam konteks pengiriman data?

HTML adalah Markup Language yang berguna untuk menampilkan dan merender halaman web ke pengguna. Data yang diberikan dalam bentuk HTML biasanya untuk user yang mengakses web melalui browser. XML juga adalah Markup Language namun lebih mudah dibaca manusia dan mesin. XML menyusun data dalam struktur hierarki (tree) yang memudahkan untuk pengiriman data. JSON adalah sebuah data interchange yang berbasis JavaScript yang terdiri atas pair key dan value (dictionary). JSON sangat ringan jika dibandingkan dengan dua Markup Language sebelumnya sehingga digunakan dalam pertukaran data antar aplikasi.

### Mengapa JSON sering digunakan dalam pertukaran data antara aplikasi web modern?

JSON sering digunakan dalam pertukaran data aplikasi web modern karena JSON lebih ringan jika dibandingkan dengan XML dan HTML sehingga lebih mudah dibaca manusia maupun mesin (lebih efisien dan fleksibel). Format JSON juga berbasis objek dan struktur data (dictionary) yang representasinya tersedia dalam berbagai bahasa pemrograman memudahkan pertukaran data antara teknologi yang berbeda.

## Screenshoot akses URL pada Postman

### Akses HTML
![alt text](images/week3/postmanhtml.jpg)

### Akses XML
![alt text](images/week3/postmanxml.jpg)

### Akses JSON
![alt text](images/week3/postmanjson.jpg)

### Akses XML by ID
![alt text](images/week3/postmanxmlbyid.jpg)

### Akses JSON by ID
![alt text](images/week3/postmanjsonbyid.jpg)

# Tugas 2

## Proses implementasi checklist tugas

### Membuat proyek Django baru
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

### Membuat aplikasi main pada proyek yang sudah dibuat
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

### Membuat model pada aplikasi main dengan nama Item
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

### Membuat sebuah fungsi pada views.py untuk dikembalikan ke dalam sebuah template HTML
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
        ## data untuk ditambahkan ke main.html
    }

    return render(request, "main.html", context)
```

### Membuat sebuah routing pada urls.py aplikasi main untuk memetakan fungsi yang telah dibuat pada views.py
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

### Melakukan routing pada proyek agar dapat menjalankan aplikasi main
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

### Bonus : Testing
Untuk testing, dilakukan testing berjalannya url di aplikasi dan kesesuaian template sesuai tutorial. Selain itu juga ada testing kesesuaian detail model item yang dibuat.
Dibuat contoh mode item pada testcase lalu dicocokkan detail dari item yang dibuat dengan yang seharusnya.
Untuk detail dapat dilihat di [sini](main/tests.py)

### Deploy ke Adaptable
Sebelum deploy ke adaptable, pertama dibuat repositori baru di Github. Lalu saya menginisiasi git di repositori lokal yang sudah dibuat. Sebelum push saya tambahkan file .gitignore untuk konfigurasi file atau folder yang harus diabaikan Git. Isi file .gitignore sama seperti pada [tutorial 0](https://pbp-fasilkom-ui.github.io/ganjil-2024/docs/tutorial-0##tutorial-unggah-proyek-ke-repositori-github). Lalu saya push repositori lokal ke repositori di Github.
Selanjutnya saya menuju website Adaptable. Saya lalu membuat app baru dengan menghubungkan dengan repositori di Github. Setting yang digunakan untuk deploy app : Python App Template, tipe basis data PostgreSQL, versi Python 3.11, start command ```python manage.py migrate && gunicorn game_inventory.wsgi```, dan HTTP Listener on PORT = Yes.

## Bagan request Client ke aplikasi Django dan responnya
![alt text](images/week2/bagan.jpg)
Ketika ada request dari user, request akan masuk ke urls.py yang akan mengambil path url yang direquest user dan mengarahkannya ke path yang sesuai. Lalu Django akan mengakses views.py sesuai path url yang dituju. Views.py akan merender kode html dari templates yang ditambahkan dengan data yang ada. Lalu Django akan mengembalikan kode html yang sudah ditambahkan data kepada user sebagai response.

## Alasan penggunaan virtual environment dan apa yang terjadi jika tidak menggunakan virtual environment
Penggunaan virtual environment bertujuan untuk membatasi proyek dari global environment python. Jika kita membuat banyak proyek dengan berbagai dependensi yang berbeda, maka lebih efektif membuat virtual environment untuk setiap proyek yang ada. Dengan terpisahnya dependensi antar proyek, maka developer dapat bekerja dengan python dan package yang versinya berbeda-beda sesuai kebutuhan proyek.
Jika tidak menggunakan virtual environment, kita tetap dapat membuat proyek Django. Namun terdapat risiko konflik dependensi antar proyek dan konflik versi package yang digunakan.

## MVC, MVT, MVVM dan perbedaan dari ketiganya
MVC : Model, View, Controller. Model sebagai pengelola logika data pada aplikasi. View menampilkan data pada user. Controller mengatur alur aplikasi dan penghubung antara model dan view.

MVT : Model, View, Template. Model sama seperti MVC mengelola logika data. View menampilkan data pada user. Template adalah kumpulan html code yang berisi tampilan  yang tidak memiliki logika. View pada MVT mengatur data yang ditambahkan ke template untuk ditampilkan kepada user.

MVVM : Model, View, ViewModel. Model dan View sama seperti MVC. ViewModel adalah abstraksi dari view dan juga dapat dideskripsikan sebagai state (keadaan) data pada model.