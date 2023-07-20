from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from ..models import Meeting

def meeting_detail(request, meeting_id):
    # Get the meeting object or return a 404 error if not found
    meeting = get_object_or_404(Meeting, id=meeting_id)
    
    # check if the meeting has already started or ended
    current_time = timezone.now()
    has_started = meeting.start_time <= current_time
    has_ended = meeting.end_time <= current_time
    
    return render(request, 'meeting_detail.html', {
        'meeting': meeting,
        'has_started': has_started,
        'has_ended': has_ended,
    })
