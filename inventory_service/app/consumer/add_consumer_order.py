from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import json
from app.db import get_session
from app.crud.inventory_crud import validate_inventory_id
from app.models.inventory_model import InventoryItem
from app import order_pb2

async def consume_order_message(topic, bootstrap_servers):
# create a consumer instance
    consumer = AIOKafkaConsumer(
        topic, 
        bootstrap_servers= bootstrap_servers,
        group_id = "OrderGroup", 
        auto_offset_reset='earliest'
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print(f"Received message on topic: {msg.topic}")
        
        #     print("\n\n RAW ORDER MESSAGE \n\n")
        #     print(f"\n\n Consumer Raw message Vaue: {msg.topic}\n")
        #     print(f"\n\n Consumer Vaue: {msg.value}\n")
            
            # through protobuf
            order_data = order_pb2.Order()
            order_data.ParseFromString(msg.value)
            inventory_id = order_data.inventory_id
            print(f"\n\nConsumer Deserialized data: {order_data}")

           # 1. Extract Inventory Id
            order_data = json.loads(msg.value.decode())
            inventory_id = order_data["inventory_id"]
            print("Inventory ID", inventory_id)
             # 2. Check if Inventory Id is Valid
            with next(get_session()) as session:
                inventory = validate_inventory_id(
                    inventory_id=inventory_id, session=session)
                print("INVENTORY VALIDATION CHECK", inventory)
                if inventory is None:
                    print(f"Inventory not found.")
                if inventory is not None:
                    print(f"Order found.")
                    producer = AIOKafkaProducer(
                        bootstrap_servers='broker:19092')
                    await producer.start()
                    try:
                        await producer.send_and_wait(
                            "orderchecking",
                             msg.value
                        )
                    finally:
                        await consumer.stop()


            
            
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()