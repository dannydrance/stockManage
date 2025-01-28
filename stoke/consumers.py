import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist
from stoke.models import Product

class RFIDConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        rfid_id = data.get("rfid_id")

        if rfid_id:
            try:
                product = Product.objects.get(card_id=rfid_id)
                await self.send(json.dumps({
                    "exists": True,
                    "deviceName": product.name,
                    "product_expired": product.expired_on.strftime("%Y-%m-%d"),
                }))
            except ObjectDoesNotExist:
                await self.send(json.dumps({
                    "exists": False,
                    "rfid_id": rfid_id,
                }))
        else:
            await self.send(json.dumps({"error": "RFID ID is missing"}))
