from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from main.forms import ItemForm
from main.models import Item
from django.urls import reverse
from django.core import serializers

# Create your views here.
def show_main(request):
    items = Item.objects.all()
    item_counter = items.count()
    item_sum = sum([item.amount for item in items])
    context = {
        'nama': 'Alwin Djuliansah',
        'kelas': 'PBP D',
        'item_sum': item_sum,
        'item_counter': item_counter,
        'items': items,
        #'name': 'The Art of War',
        #'amount': 1,
        #'description': 'The ancient Chinese military text, dating from the Late Spring and Autumn Period, was written by Sun Tzu.',
    }

    return render(request, "main.html", context)
    
def create_item(request):
    form = ItemForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
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