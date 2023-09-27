import datetime
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from main.forms import ItemForm
from main.models import Item
from django.urls import reverse
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  

# Create your views here.
@login_required(login_url='/login')
def show_main(request):
    items = Item.objects.filter(user=request.user)
    item_counter = items.count()
    item_sum = sum([item.amount for item in items])
    context = {
        'nama': request.user.username,
        'kelas': 'PBP D',
        'item_sum': item_sum,
        'item_counter': item_counter,
        'items': items,
        'last_login': request.COOKIES['last_login'],
        #'name': 'The Art of War',
        #'amount': 1,
        #'description': 'The ancient Chinese military text, dating from the Late Spring and Autumn Period, was written by Sun Tzu.',
    }

    return render(request, "main.html", context)

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

def create_item(request):
    form = ItemForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        item = form.save(commit=False)
        item.user = request.user
        item.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "create_item.html", context)



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