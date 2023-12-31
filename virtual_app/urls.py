# urls.py

from django.urls import path, re_path
from .endpoints.home import home
from .endpoints.create_meeting import create_meeting
from .endpoints.join_meeting import join_meeting, meeting_room
from .endpoints.list_participants import list_participants
from .endpoints.list_recordings import list_recordings
from .endpoints.meeting_detail import meeting_detail
from .endpoints.profile import profile

app_name = 'virtual_app'

urlpatterns = [
    # Home page
    path('', home, name='home'),

    # Meeting related URLs
    path('meeting/create/', create_meeting, name='create_meeting'),
    path('meeting/<int:meeting_id>/', meeting_detail, name='meeting_detail'),
    path('meeting/<int:meeting_id>/join/', join_meeting, name='join_meeting'),

    # Update the meeting_room URL pattern with a regex to capture the participant_token
    re_path(r'^meeting/(?P<meeting_id>[0-9]+)/room/(?P<participant_token>[A-Za-z0-9_]+)/$', meeting_room, name='meeting_room'),

    # Participant related URLs
    path('meeting/<int:meeting_id>/participants/', list_participants, name='list_participants'),

    # Recording related URLs
    path('meeting/<int:meeting_id>/recordings/', list_recordings, name='list_recordings'),

    # User related URLs (for example, profile)
    path('profile/', profile, name='profile'),
]
