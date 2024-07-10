# app/consumer.py
from aiokafka import AIOKafkaConsumer
from app.db import get_session
from app.crud.order_crud import add_new_order
from app.models.order_model import Order
import json
from app import order_pb2
async def consume_message(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="Order_Consumer"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print(f"\n\n Received Raw message on topic: {msg.topic}\n\n")
            ## Through Json Format
            # order_data = json.loads(msg.value.decode())
            # print("TYPE", (type(order_data)))
            # print(f"Order Data {order_data}")
            # print(f"\n\n Consumer Raw message Vaue: {msg.topic}\n")

            # with next(get_session()) as session:
            #     print("SAVING DATA TO DATABSE")
            #     db_insert_order = add_new_order(
            #         order=Order(**order_data), session=session)
            #     print("DB_INSERT_ORDER", db_insert_order)

            order = order_pb2.Order()
            order.ParseFromString(msg.value)
            print(f"User Data: {order}")
            order = Order(id=order.id, inventory_id = order.inventory_id, quantity=order.quantity, total_price = order.total_price, status=order.status)
            with next(get_session()) as session:
                db_insert_order = add_new_order(order=order, session=session)
                print(f"DB_INSERT_Order: {db_insert_order}")
                
    finally:
        await consumer.stop()
