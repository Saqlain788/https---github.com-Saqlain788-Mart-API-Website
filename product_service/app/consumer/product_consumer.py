from aiokafka import AIOKafkaConsumer
# import json
from app.db import get_session
from app.crud.product_crud import add_new_product
from app.models.product_model import Product
from app import product_pb2

async def consume_message(topic, bootstrap_servers):
# create a consumer instance
    consumer = AIOKafkaConsumer(
        topic, 
        bootstrap_servers= bootstrap_servers,
        group_id = "ProductGroup",
        auto_offset_reset='earliest'
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print(f"Received message on topic: {msg.topic}")

            # product_data = json.loads(msg.value.decode())
            # print("TYPE", (type(product_data)))
            # print(f"Product Data {product_data}")
            # print(f"\n\n Consumer Raw message Vaue: {msg.topic}")
            # with next(get_session()) as session:
            #     print("SAVING DATA TO DATABSE")
            #     db_insert_product = add_new_product(
            #         product_data=Product(**product_data), session=session)
            #     print("DB_INSERT_PRODUCT", db_insert_product)
            
            new_product = product_pb2.Product()
            new_product.ParseFromString(msg.value)
            print(f"\n\n Consumer Deserialized data: {new_product}")
            product_data = Product(id=new_product.id,  name=new_product.name, description=new_product.description, price=new_product.price, quantity=new_product.quantity, brand=new_product.brand, weight=new_product.weight, category=new_product.category)
            with next(get_session()) as session:
                print("SAVING DATA TO DATABSE")
                # Add new product
                db_insert_product = add_new_product(
                    product_data=product_data, session=session)
                print("DB_INSERT_PRODUCT", db_insert_product)
                db_insert_product = add_new_product(
                    product_data=Product(**product_data), session=session)
                print("DB_INSERT_PRODUCT", db_insert_product)
                
                # Event EMIT In NEW TOPIC

            # Here you can add code to process each message.
            # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()
