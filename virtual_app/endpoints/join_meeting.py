from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from ..models import Meeting
from datetime import datetime
from django.utils import timezone
import random
import string
from .forms import ParticipantForm

@login_required
def join_meeting(request, meeting_id):
    # Get the meeting object or return a 404 error if not found
    meeting = get_object_or_404(Meeting, id=meeting_id)
    
    # Convert the current time to the timezone of the meeting start time
    current_time = timezone.localtime(timezone.now())

    # Convert the meeting start time to the same timezone format as current_time
    meeting_start_time = timezone.localtime(meeting.start_time)

    # Check if the meeting has already started or ended
    has_started = current_time >= meeting_start_time
    has_ended = meeting.end_time <= current_time

    if not has_started:
        # Meeting has not started yet
        return render(request, 'not_started.html', {'meeting': meeting})
    
    if has_ended:
        # Meeting has already ended
        return render(request, 'ended.html', {'meeting': meeting})
    
    if request.method == 'POST':
        # Process the form submission
        form = ParticipantForm(request.POST)
        
        if form.is_valid():
            # The form data is valid, process the participant's details here
            participant_name = form.cleaned_data['participant_name']
            
            # Save the participant's details to the database or handle as needed
            
            # Generate a unique participant token (similar to the previous implementation)
            participant_token = generate_token(request.user)
            
            # Redirect to the meeting room with the participant_token as a query parameter
            return redirect('virtual_app:meeting_room', meeting_id=meeting_id, participant_token=participant_token)
    else:
        # If it's a GET request, display the form for the user to enter their details
        form = ParticipantForm()

    return render(request, 'join_meeting.html', {
        'meeting': meeting,
        'form': form,
    })

@login_required
def meeting_room(request, meeting_id, participant_token):
    # Get the meeting object or return a 404 error if not found
    meeting = get_object_or_404(Meeting, id=meeting_id)
    
    # Check if the participant is the host
    is_host = meeting.host == request.user
    
    return render(request, 'meeting_room.html', {
        'meeting': meeting,
        'participant_token': participant_token,
        'is_host': is_host,
    })

def generate_token(user):
    # Generate a random alphanumeric token
    length = 10
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    # Add the user's username to the token for uniqueness
    token += f"_{user.username}"
    
    return token
