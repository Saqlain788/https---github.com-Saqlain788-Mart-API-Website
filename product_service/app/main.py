from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from aiokafka import AIOKafkaProducer 
import json
import asyncio 
from app import product_pb2

from app.models.product_model import Product, updatedproduct
from app.db import get_session, engine, create_db_and_tables
from contextlib import asynccontextmanager
from app.crud.product_crud import add_new_product, get_all_products, get_product_by_id, delete_product_by_id, update_product_by_id
from app.producer import get_kafka_producer
from typing import Annotated, AsyncGenerator
from app import settings
from app.consumer.product_consumer import consume_message
from app.consumer.inventory_consumer import consume_inventory_message 
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating table")
    task = asyncio.create_task(consume_message
    (settings.KAFKA_PRODUCT_TOPIC,'broker:19092'))
    asyncio.create_task(consume_inventory_message
    ("AddStocks", 'broker:19092'))
    
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "Product Service1"}

@app.post("/products/", response_model=Product)
async def create_new_product(product: Product, session: Annotated[Session, Depends(get_session)], producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    # product_dict = {field: getattr(product, field) for field in product.dict()}
    # product_dict = {field: getattr(product, field) for field in product.dict()}
    # product_json = json.dumps(product_dict).encode("utf-8")
    # print("product_JSON:", product_json)
    # await producer.send_and_wait(settings.KAFKA_PRODUCT_TOPIC, product_json)
    # Produce message
    product_protobuf = product_pb2.Product(id=product.id, name=product.name, description=product.description, price=product.price, quantity=product.quantity, brand=product.brand, weight=product.weight, category=product.category)
    print(f"Product Protobuf: {product_protobuf}")
    # Serialize the message to a byte string
    serialized_product = product_protobuf.SerializeToString()
    print(f"Serialized data: {serialized_product}")
    await producer.send_and_wait(settings.KAFKA_PRODUCT_TOPIC, serialized_product)
    return product

    # new_product = add_new_product(product, session)
    # return new_product

@app.get("/products/all", response_model=list[Product])
def get_all_products_from_db(session: Annotated[Session, Depends(get_session)]):
    product = get_all_products(session)
    return product

@app.get("/products/{product_id}", response_model=Product)
def get_single_product_by_id(product_id: int, session: Annotated[Session, Depends(get_session)]):
    try:
        return get_product_by_id(product_id=product_id, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.delete("/products/{product_id}", response_model= Product)
def delete_single_product_by_id(product_id: int, session: Annotated[Session, Depends(get_session)]):
    try:
        return delete_product_by_id(product_id=product_id, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.patch("/products/{product_id}", response_model=Product)
def update_signle_product_by_id(product_id: int, product: updatedproduct, session: Annotated[Session, Depends(get_session)]):
    try:
        return update_product_by_id(product_id=product_id, to_update_product_data=product, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
