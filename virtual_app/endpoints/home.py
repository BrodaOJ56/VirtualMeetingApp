from django.shortcuts import render

def home(request):
    # Implement your home view logic here
    return render(request, 'virtual_app/home.html')
