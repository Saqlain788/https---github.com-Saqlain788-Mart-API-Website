# from aiokafka import AIOKafkaProducer
from aiokafka import AIOKafkaProducer
# # Kafka Producer as a dependency
async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers='broker:19092')
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()


