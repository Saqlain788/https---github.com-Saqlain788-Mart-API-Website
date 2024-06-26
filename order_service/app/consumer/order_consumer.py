# app/consumer.py
from aiokafka import AIOKafkaConsumer
from app.db import get_session
from app.crud.order_crud import add_new_order
from app.models.order_model import Order
import json

async def consume_message(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="my-order-consumer-group"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print(f"\n\n Received Raw message on topic: {msg.topic}\n\n")
            ## Through Json Format
            order_data = json.loads(msg.value.decode())
            print("TYPE", (type(order_data)))
            print(f"Product Data {order_data}")

            with next(get_session()) as session:
                print("SAVING DATA TO DATABSE")
                db_insert_order = add_new_order(
                    order=Order(**order_data), session=session)
                print("DB_INSERT_PRODUCT", db_insert_order)

        
    finally:
        await consumer.stop()
