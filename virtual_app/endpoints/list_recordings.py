from django.shortcuts import render, get_object_or_404
from ..models import Meeting, MeetingRecording

def list_recordings(request, meeting_id):
    # Get the meeting object or return a 404 error if not found
    meeting = get_object_or_404(Meeting, id=meeting_id)
    
    # Get the recordings for the meeting
    recordings = MeetingRecording.objects.filter(meeting=meeting)
    
    # Implement other recording list view logic here
    return render(request, 'virtual_app/list_recordings.html', {'meeting': meeting, 'recordings': recordings})
