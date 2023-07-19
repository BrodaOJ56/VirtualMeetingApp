from django.shortcuts import render, get_object_or_404
from ..models import Meeting
from datetime import datetime
import random
import string

def join_meeting(request, meeting_id):
    # Get the meeting object or return a 404 error if not found
    meeting = get_object_or_404(Meeting, id=meeting_id)
    
    # Check if the meeting has already started or ended
    current_time = datetime.now()
    has_started = meeting.start_time <= current_time
    has_ended = meeting.end_time <= current_time
    
    if not has_started:
        # Meeting has not started yet
        return render(request, 'virtual_app/not_started.html', {'meeting': meeting})
    
    if has_ended:
        # Meeting has already ended
        return render(request, 'virtual_app/ended.html', {'meeting': meeting})
    
    # Generate a unique token for the participant joining the meeting
    participant_token = generate_token(request.user)
    
    return render(request, 'virtual_app/join_meeting.html', {
        'meeting': meeting,
        'participant_token': participant_token,
    })

def generate_token(user):
    # Generate a random alphanumeric token
    length = 10
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    # Add the user's username to the token for uniqueness
    token += f"_{user.username}"
    
    return token
