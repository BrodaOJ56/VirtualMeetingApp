from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    user = request.user
    # fetch user-related data from the database or any other data source
    user_data = {
        'username': user.username,
        'email': user.email,
        # Add more user-related data fields as needed
    }
    
    return render(request, 'profile.html', {'user_data': user_data})
