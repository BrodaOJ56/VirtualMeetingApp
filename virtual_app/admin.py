from django.contrib import admin
from .models import Meeting, Participant, MeetingRecording
# Register your models here.

admin.site.register(Meeting)
admin.site.register(Participant)
admin.site.register(MeetingRecording)
