# kafka_consumer.py
from aiokafka import AIOKafkaConsumer
import json
from app import user_pb2
from app.db import get_session
from app.crud.user_crud import create_user
from app.models.user_model import UserCreate

async def consume_notification_message(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic, 
        bootstrap_servers=bootstrap_servers,
        group_id="NotificationUserGroup"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print(f"Received message on topic: {msg.topic}")
            # user_data = json.loads(msg.value.decode())
            # print(f"User Data: {user_data}")
            # with next(get_session()) as session:
            #     create_user(UserCreate(**user_data), session)
            user = user_pb2.UserCreate()
            user.ParseFromString(msg.value)
            print(f"User Data: {user}")
            user_data = UserCreate(order_id = user.order_id, name = user.name, email = user.email, password = user.password)
            with next(get_session()) as session:
                db_insert_user = create_user(user=user_data, session=session)
                print(f"DB_INSERT_USER: {db_insert_user}")
                # db_insert_user = create_user(user=UserCreate(**user_data), session=session)
                # print(f"DB_INSERT_USER: {db_insert_user}")

    finally:
        await consumer.stop()
