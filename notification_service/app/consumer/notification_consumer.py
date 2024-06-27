# kafka_consumer.py
from aiokafka import AIOKafkaConsumer
import json
from app.db import get_session
from app.crud.notification_crud import create_notification
from app.models.notification_model import NotificationCreate

async def consume_message(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="notification-consumer-group"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print(f"Received message on topic: {msg.topic}")
            notification_data = json.loads(msg.value.decode())
            with next(get_session()) as session:
                notification_create = NotificationCreate(**notification_data)
                create_notification(notification_create, session)
    finally:
        await consumer.stop()
