from django.shortcuts import render, redirect
from ..models import Meeting

def create_meeting(request):
    if request.method == 'POST':
        # Process form submission and create a new meeting
        title = request.POST.get('title')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        
        # Perform necessary validation (you can add more validation if needed)
        if title and start_time and end_time:
            # All required fields are present, create the meeting object
            host_id = request.user.id  # Get the ID of the authenticated user (the host)
            meeting = Meeting.objects.create(title=title, start_time=start_time, end_time=end_time, host_id=host_id)
            # Redirect to the meeting detail page or any other desired page
            return redirect('virtual_app:meeting_detail', meeting_id=meeting.id)
        else:
            # Form data is incomplete, show an error message or handle accordingly
            return render(request, 'create_meeting.html', {'error': 'All fields are required!'})
    
    # If the request method is not POST, display the create meeting form template
    return render(request, 'create_meeting.html')
