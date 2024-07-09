from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, SQLModel
from aiokafka import AIOKafkaProducer
import asyncio
from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator
import json

from app.models.order_model import Order, UpdatedOrder
from app.db import get_session, create_db_and_tables
from app.crud.order_crud import  get_all_orders, get_order_by_id, delete_order_by_id, update_order_by_id
from app.producer import get_kafka_producer
from app import order_pb2
from app.consumer.order_consumer import consume_message
from app.consumer.user_consumer import consume_user_message


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables....................")
    
    # Start the Kafka consumer for Order Service
    task = asyncio.create_task(consume_message("orderchecking", 'broker:19092'))
    asyncio.create_task(consume_user_message("UserCreated", 'broker:19092'))

    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan, title="Order Service API", version="0.0.1")

@app.get("/")
def read_root():
    return {"Hello": "Order Service"}

@app.post("/manage-order/", response_model=Order)
async def create_order(order: Order, session: Annotated[Session, Depends(get_session)], producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    # json format
    # order_dict = {field: getattr(order, field) for field in order.dict()}
    # order_json = json.dumps(order_dict).encode("utf-8")
    # print("product_JSON:", order_dict)
    # # Produce message 
    # await producer.send_and_wait("Ordertopic", order_json)
    # return order
    order_protobuf = order_pb2.Order(id=order.id, inventory_id = order.inventory_id, quantity=order.quantity, total_price = order.total_price, status=order.status)
    print(f"Order Protobuf: {order_protobuf}")
    # Serialize the message to a byte string
    serialized_order = order_protobuf.SerializeToString()
    print(f"Serialized data: {serialized_order}")
    await producer.send_and_wait("Ordertopic", serialized_order)
    return order
    
@app.get("/manage-order/all", response_model=list[Order])
def get_all_orders_from_db(session: Annotated[Session, Depends(get_session)]):
    try:
        orders = get_all_orders(session)
        # print("Fetched orders from DB:", orders)
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/manage-order/{order_id}", response_model=Order)
def get_orderby_id(order_id: int, session: Annotated[Session, Depends(get_session)]):
    try:
        return get_order_by_id(order_id=order_id, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/manage-order/{order_id}", response_model=dict)
def delete_single_order_by_id(order_id: int, session: Annotated[Session, Depends(get_session)]):
    try:
        return delete_order_by_id(order_id=order_id, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/manage-order/{order_id}", response_model=Order)
def updates_single_order_by_id(order_id: int, order: UpdatedOrder, session: Annotated[Session, Depends(get_session)]):
    try:
        return update_order_by_id(order_id=order_id, to_update_order_data=order, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
