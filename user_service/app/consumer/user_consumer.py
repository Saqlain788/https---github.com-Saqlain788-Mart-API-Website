# kafka_consumer.py
from aiokafka import AIOKafkaConsumer
import json

from app.db import get_session
from app.crud.user_crud import create_user
from app.models.user_model import UserCreate

async def consume_message(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic, 
        bootstrap_servers=bootstrap_servers,
        group_id="my-user-consumer-group"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print(f"Received message on topic: {msg.topic}")
            user_data = json.loads(msg.value.decode())
            print(f"User Data: {user_data}")
            with next(get_session()) as session:
                create_user(UserCreate(**user_data), session)
    finally:
        await consumer.stop()
