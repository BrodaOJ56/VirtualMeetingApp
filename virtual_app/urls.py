from django.urls import path
from . import views

app_name = 'virtual_app'

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # Meeting related URLs
    path('meeting/create/', views.create_meeting, name='create_meeting'),
    path('meeting/<int:meeting_id>/', views.meeting_detail, name='meeting_detail'),
    path('meeting/<int:meeting_id>/join/', views.join_meeting, name='join_meeting'),

    # Participant related URLs
    path('meeting/<int:meeting_id>/participants/', views.list_participants, name='list_participants'),

    # Recording related URLs
    path('meeting/<int:meeting_id>/recordings/', views.list_recordings, name='list_recordings'),

    # User related URLs (for example, profile)
    path('profile/', views.profile, name='profile'),
]
