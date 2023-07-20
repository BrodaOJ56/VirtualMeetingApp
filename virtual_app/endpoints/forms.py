# forms.py

from django import forms

class ParticipantForm(forms.Form):
    participant_name = forms.CharField(max_length=100, required=True, label='Your Name')
    # Add other fields as needed
