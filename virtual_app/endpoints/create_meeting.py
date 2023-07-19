from django.shortcuts import render, redirect
from ..models import Meeting

def create_meeting(request):
    if request.method == 'POST':
        # Process form submission and create a new meeting
        title = request.POST.get('title')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        
        # Perform necessary validation and create the meeting object
        meeting = Meeting.objects.create(title=title, start_time=start_time, end_time=end_time)
        
        # Redirect to the meeting detail page or any other desired page
        return redirect('virtual_app:meeting_detail', meeting_id=meeting.id)
    
    # Render the create meeting form template
    return render(request, 'virtual_app/create_meeting.html')
