import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MeetingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f"meeting_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Handles incoming WebSocket messages.
        Expected message format: {"type": "offer/answer/candidate", "sdp/candidate": "..."}
        """
        data = json.loads(text_data)
        msg_type = data.get("type")

        if msg_type in ["offer", "answer", "candidate"]:
            # Broadcast signaling message to all peers in the room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "signal_message",
                    "message": data,
                    "sender": self.channel_name,  # track sender
                }
            )

    async def signal_message(self, event):
        """
        Sends signaling messages to all peers except the sender.
        """
        if event["sender"] != self.channel_name:
            await self.send(text_data=json.dumps(event["message"]))
