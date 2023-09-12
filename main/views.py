from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'nama': 'Alwin Djuliansah',
        'kelas': 'PBP D',
        'name': 'The Art of War',
        'amount': 1,
        'description': 'The ancient Chinese military text, dating from the Late Spring and Autumn Period, was written by Sun Tzu.',
    }

    return render(request, "main.html", context)