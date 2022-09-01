import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class TicTacToeConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = 'room_%s'%self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        print('Disconnected')

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Receive message from WebSocket.
        Get the event and send the appropriate event
        """
        response = json.loads(text_data)
        event = response.get("event", None)
        message = response.get("message", None)
        winner = response.get('winner', None)
        image = response.get('image', None)

        if event == 'MOVE':
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                "event": "MOVE",
            })

        if event == 'START':
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                'event': "START",
            })

        if event == 'END':
            # Send message to room group

            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                'event': "END",
                'winner': winner,
                'image': image
            })
            

    async def send_message(self, res):
        """ Receive message from room group """
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "payload": res,
        }))


class PixelBattleConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'pixelBattle'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        print('Disconnected')

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Receive message from WebSocket.
        Get the event and send the appropriate event
        """
        response = json.loads(text_data)
        positionX = response.get("positionX", None)
        positionY = response.get("positionY", None)
        event = response.get('event', None)
        color = response.get('color')

        # Send message to room group
        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'send_message',
            'event': event,
            'positionX': positionX,
            "positionY": positionY,
            'color': color,
        })

            

    async def send_message(self, res):
        await self.send(text_data=json.dumps({
            "payload": res,
        }))