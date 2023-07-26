from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

class Meeting(models.Model):
    title = models.CharField(max_length=255)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    meeting_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    invitation_link = models.CharField(max_length=50, unique=True, blank=True, null=True)



    def save(self, *args, **kwargs):
        if not self.invitation_link:
            # Generate a unique invitation link for the meeting
            self.invitation_link = get_random_string(length=20)  # You can adjust the length as needed
        super().save(*args, **kwargs)

        
    def __str__(self):
        return self.title


class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_host = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.meeting.title}"


class MeetingRecording(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    recording_file = models.FileField(upload_to='meeting_recordings/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.meeting.title
