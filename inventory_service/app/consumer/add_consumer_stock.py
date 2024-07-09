from aiokafka import AIOKafkaConsumer
import json

from app.db import get_session
from app.crud.inventory_crud import add_new_inventory_item
from app.models.inventory_model import InventoryItem
from app import inventory_pb2

async def consume_message(topic, bootstrap_servers):
# create a consumer instance
    consumer = AIOKafkaConsumer(
        topic, 
        bootstrap_servers= bootstrap_servers,
        group_id = "StockGroup"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print(f"Received message on topic: {msg.topic}")
            ## Through Json Format
            # inventory_item = json.loads(msg.value.decode())
            # print("TYPE", (type(inventory_item)))
            # print(f"Inventory Data {inventory_item}")
            # print(f"\n\n Consumer Raw message Vaue: {msg.topic}\n")

            # with next(get_session()) as session:
            #     print("SAVING DATA TO DATABSE")
            #     db_insert_inventory = add_new_inventory_item(
            #         inventory_item=InventoryItem(**inventory_item), session=session)
            #     print("DB_INSERT_PRODUCT", db_insert_inventory)

            ## Through Protobuf Format
            inventory_item = inventory_pb2.InventoryItem()
            inventory_item.ParseFromString(msg.value)
            print(f"Product Data, {inventory_item}")
            inventory_stock = InventoryItem(id=inventory_item.id, product_id=inventory_item.product_id, variant_id=inventory_item.variant_id, quantity=inventory_item.quantity, status=inventory_item.status)    
            with next(get_session()) as session:
                print("SAVING DATA TO DATABSE")
                db_insert_inventory = add_new_inventory_item(
                    inventory_item=inventory_stock, session=session)
                print("DB_INSERT_PRODUCT", db_insert_inventory)

                    # Event EMIT In NEW TOPIC

            # Here you can add code to process each message.
            # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()

