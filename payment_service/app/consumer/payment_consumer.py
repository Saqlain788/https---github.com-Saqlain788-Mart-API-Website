from aiokafka import AIOKafkaConsumer
from app.db import get_session
from app.models.payment_model import Payment
from app.crud.payment_crud import create_payment
import json

async def consume_payment_message(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="payment-service-consumer-group"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            payment_data = json.loads(msg.value.decode())
            print(f"Received payment processed event: {payment_data}")
            payment = Payment(**payment_data)
            with next(get_session()) as session:
                create_payment(payment, session)
    finally:
        await consumer.stop()
