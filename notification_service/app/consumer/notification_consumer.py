# kafka_consumer.py
from aiokafka import AIOKafkaConsumer
import json
from app.db import get_session
from app.crud.notification_crud import create_notification
from app.models.notification_model import NotificationCreate
from app import notification_pb2
async def consume_message(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="NotificationGroup"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            notification = notification_pb2.NotificationCreate()
            notification.ParseFromString(msg.value)
            print(f"payment Data: {notification}")
            notification_detail = NotificationCreate(user_id=notification.user_id, message=notification.message, status=notification.status)
            with next(get_session()) as session:
                db_insert_notification = create_notification(notification==notification_detail, session=session)
                print(f"DB_INSERT_Payment: {db_insert_notification}")
            
    finally:
        await consumer.stop()
