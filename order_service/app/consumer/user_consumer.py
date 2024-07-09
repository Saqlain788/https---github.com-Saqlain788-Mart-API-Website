# app/consumer.py
from aiokafka import AIOKafkaConsumer
from app.db import get_session
from app.crud.order_crud import validate_order_id
from app.models.order_model import Order
import json

async def consume_user_message(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="UserGroup",
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print(f"Received message on topic: {msg.topic}")

            print("\n\n RAW USER MESSAGE \n\n")
            print(f"\n\n Consumer Raw message Vaue: {msg.topic}\n")
            print(f"\n\n Consumer Vaue: {msg.value}\n")

           # 1. Extract Order Id
            user_data = json.loads(msg.value.decode())
            order_id = user_data["order_id"]
            print("ORDER ID", order_id)
             # 2. Check if Product Id is Valid
            with next(get_session()) as session:
                order = validate_order_id(
                    order_id=order_id, session=session)
                print("ORDER VALIDATION CHECK", order)
                if order is None:
                    print(f"Order not found.")
                if order is not None:
                    print(f"Order found.")
                    producer = AIOKafkaProducer(
                        bootstrap_servers='broker:19092')
                    await producer.start()
                    try:
                        await producer.send_and_wait(
                            "user-add-processed-response",
                            msg.value
                        )
                    finally:
                        await consumer.stop()
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()