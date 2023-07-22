import json
from channels.generic.websocket import AsyncWebsocketConsumer

class VideoCallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the meeting_id from URL path and create a unique group name
        meeting_id = self.scope['url_route']['kwargs']['meeting_id']
        self.meeting_group_name = f'meeting_{meeting_id}'

        # Add the WebSocket to the meeting group
        await self.channel_layer.group_add(
            self.meeting_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Remove the WebSocket from the meeting group
        await self.channel_layer.group_discard(
            self.meeting_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Handle incoming signaling messages
        data = json.loads(text_data)
        message_type = data['type']
        if message_type == 'offer' or message_type == 'answer':
            # Broadcast the offer/answer to all participants
            await self.channel_layer.group_send(
                self.meeting_group_name,
                {
                    'type': 'send_message',
                    'message': data
                }
            )
        elif message_type == 'ice_candidate':
            # Broadcast ICE candidate to all participants
            await self.channel_layer.group_send(
                self.meeting_group_name,
                {
                    'type': 'send_message',
                    'message': data
                }
            )

    async def send_message(self, event):
        # Send the signaling message to the WebSocket
        message = event['message']
        await self.send(text_data=json.dumps(message))
