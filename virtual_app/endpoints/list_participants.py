from django.shortcuts import render, get_object_or_404
from ..models import Meeting, Participant

def list_participants(request, meeting_id):
    # Get the meeting object or return a 404 error if not found
    meeting = get_object_or_404(Meeting, id=meeting_id)
    
    # Get the participants for the meeting
    participants = Participant.objects.filter(meeting=meeting)
    
    # Implement other participant list view logic here
    return render(request, 'virtual_app/list_participants.html', {'meeting': meeting, 'participants': participants})
