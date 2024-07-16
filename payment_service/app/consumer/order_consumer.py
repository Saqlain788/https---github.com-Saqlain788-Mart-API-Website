from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from app.db import get_session
from app.models.payment_model import Payment, PaymentCreate
from app.crud.payment_crud import create_payment, validate_payment_id
import json
from app import order_pb2
async def consume_payment_message(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="PaymentGroup"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print(f"Received message on topic: {msg.topic}")
            
            order_data = order_pb2.OrderCreate()
            order_data.ParseFromString(msg.value)
            print(f"Deserialized Order Data: {order_data}")
            payment_id = order_data.payment_id
            print(f"Payment ID: {payment_id}")
            # payment_detail = Payment(user_id=payment.user_id, order_id=payment.order_id, amount=payment.amount, status=payment.status)
            
            with next(get_session()) as session:
                payment = validate_payment_id(payment_id=payment_id, session=session)
                if payment is None: 
                    print("Payment not found. Creating new payment...")            
                # else:
                #     print(f"Payment found.")
                #     producer = AIOKafkaProducer(bootstrap_servers='broker:19092')
                #     await producer.start()
                #     try:
                #         await producer.send_and_wait("PaymentReceived", msg.value)
                #     finally:
                #         await producer.stop()
    finally:
        await consumer.stop()
