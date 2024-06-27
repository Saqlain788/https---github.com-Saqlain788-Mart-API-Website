from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import json
from app.db import get_session
from app.crud.product_crud import add_new_product, validate_product_id
from app.models.product_model import Product
from app import product_pb2


async def consume_inventory_message(topic, bootstrap_servers):
# create a consumer instance
    consumer = AIOKafkaConsumer(
        topic, 
        bootstrap_servers= bootstrap_servers,
        group_id = "inventory-add-stock-consumer-group",
        # auto_offset_reset='earliest'
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print(f"Received message on topic: {msg.topic}")

            # print("TYPE", (type(product_data)))
            # print(f"Product Data {product_data}")
            print("\n\n RAW INVENTORY MESSAGE \n\n")
            print(f"\n\n Consumer Raw message Vaue: {msg.topic}\n")
            print(f"\n\n Consumer Vaue: {msg.value}\n")

            # 1. Extract Poduct Id
            inventory_data = json.loads(msg.value.decode())
            product_id = inventory_data["product_id"]
            print("PRODUCT ID", product_id)

            # 2. Check if Product Id is Valid
            with next(get_session()) as session:
                product = validate_product_id(
                    product_id=product_id, session=session)
                print("PRODUCT VALIDATION CHECK", product)
            
            # Protobuf method 

            # inventory_data = product_pb2.Product()
            # inventory_data.ParseFromString(msg.value)
            # product_id = inventory_data.id
            # print(f"\n\n Consumer Deserialized data: {inventory_data}")

            # 2. Check if Product Id is Valid
            # with next(get_session()) as session:
            #     product = validate_product_id(product_id=product_id, session=session)
            #     print("PRODUCT VALIDATION CHECK", product)
            # 3. if valid, 
                #   write New topic    
                if product is not None:
                    print("Product Validation check passed")
                    producer = AIOKafkaProducer(
                        bootstrap_servers='broker:19092',
                    )
                    print("Producer test")
                    await producer.start()
                    print("producer started")
                    try:
                        print("Sending message to topic: new-inventory-topic")
                        await producer.send_and_wait(
                            topic="inventory-add-stock-response",
                            value=inventory_data.SerializeToString(),
                        )
                    finally:
                        await producer.stop()
        
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()
