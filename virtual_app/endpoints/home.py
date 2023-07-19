from django.shortcuts import render

def home(request):
    # Get any necessary data or perform calculations
    data = {
        'message': 'Welcome to the Virtual App!'
    }
    
    # Render the template with the data
    return render(request, 'virtual_app/home.html', context=data)
