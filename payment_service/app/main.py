# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, SQLModel
from aiokafka import AIOKafkaProducer 
import json
import asyncio
from contextlib import asynccontextmanager
from typing import List, Annotated, AsyncGenerator
from app import payment_pb2
from app.models.payment_model import Payment, PaymentCreate, PaymentUpdate
from app.db import get_session, engine
from app.crud.payment_crud import create_payment, get_all_payments, get_payment_by_id, update_payment_by_id, delete_payment_by_id
from app.producer import get_kafka_producer
from app.consumer.order_consumer import consume_payment_message
from app import settings

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Creating tables.........")
    
    task = asyncio.create_task(consume_payment_message("orderplaced", "broker:19092"))
    create_db_and_tables()
    try:
        yield
    finally:
        task.cancel()
        await task

app = FastAPI(lifespan=lifespan, title="Payment Service API", version="0.0.1")

@app.get("/")
def read_root():
    return {"Hello": "Payment Service"}

@app.post("/payments/", response_model=Payment)
async def create_new_payment(
    payment: PaymentCreate,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
):
    # db_payment = create_payment(payment, session)
    # payment_data = {
    #     "id": db_payment.id,
    #     "user_id": db_payment.user_id,
    #     "order_id": db_payment.order_id,
    #     "amount": db_payment.amount,
    #     "status": db_payment.status,
    #     "created_at": db_payment.created_at.isoformat()
    # }
    # payment_json = json.dumps(payment_data).encode("utf-8")
    # await producer.send_and_wait("PaymentProcessed", payment_json)
    # return db_payment
    payment_protobuf = payment_pb2.Payment(user_id = payment.user_id, order_id=payment.order_id, amount=payment.amount, status=payment.status)
    print(f"Payment: {payment_protobuf}")
    serialized_payment = payment_protobuf.SerializeToString()
    await producer.send_and_wait("PaymentReceived", serialized_payment)
    return payment
@app.get("/payments/", response_model=List[Payment])
def all_payments(session: Annotated[Session, Depends(get_session)]):
    return get_all_payments(session)

@app.get("/payments/{payment_id}", response_model=Payment)
def single_payment(payment_id: int, session: Annotated[Session, Depends(get_session)]):
    try:
        return get_payment_by_id(payment_id=payment_id, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/payments/{payment_id}", response_model=Payment)
def update_payment(payment_id: int, payment: PaymentUpdate, session: Annotated[Session, Depends(get_session)]):
    try:
        return update_payment_by_id(payment_id=payment_id, to_update_payment_data=payment, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/payments/{payment_id}", response_model=dict)
def delete_payment(payment_id: int, session: Annotated[Session, Depends(get_session)]):
    try:
        return delete_payment_by_id(payment_id=payment_id, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
