# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from aiokafka import AIOKafkaProducer 
import json
import asyncio 
from sqlmodel import SQLModel

from typing import List
from app.models.inventory_model import InventoryItem, UpdatedInventoryItem
from app.db import get_session, engine
from contextlib import asynccontextmanager
from app.crud.inventory_crud import  get_all_inventory_items, get_inventory_item_by_id, delete_inventory_item_by_id, update_inventory_item_by_id
from app.producer import get_kafka_producer
from typing import Annotated, AsyncGenerator
from app import settings
from app.consumer.add_consumer_stock import consume_message 
from app import inventory_pb2

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Creating table.....")

    task = asyncio.create_task(consume_message("AddStocks",'broker:19092'))
    
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan, title= "Inventory Service API", version="0.0.1")

@app.get("/")
def read_root():
    return {"Hello": "Inventory Service"}

@app.post("/manage-inventory/", response_model=InventoryItem)
async def add_new_inventory(inventory: InventoryItem, session: Annotated[Session, Depends(get_session)], producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    # inventory_dict = {field: getattr(inventory, field) for field in inventory.dict()}
    # inventory_json = json.dumps(inventory_dict).encode("utf-8")
    # print("product_JSON:", inventory_json)
    # # Produce message 
    # await producer.send_and_wait("Add-Stocks", inventory_json)
    # return inventory
    # Through Protobuf
    inventory_protobuf = inventory_pb2.InventoryItem(id=inventory.id, product_id=inventory.product_id, variant_id=inventory.variant_id, quantity=inventory.quantity, status=inventory.status)
    print(f"Product Protobuf: {inventory_protobuf}")
    # Serialize the message to a byte string
    serialized_product = inventory_protobuf.SerializeToString()
    print(f"Serialized data: {serialized_product}")
    await producer.send_and_wait("AddStocks", serialized_product)
    return inventory

    # new_product = add_new_product(product, session)
    # return new_product

@app.get("/manage-inventory/all", response_model=list[InventoryItem])
def all_inventory_items(session: Annotated[Session, Depends(get_session)]):
    """ Get all inventory items from the database"""
    return get_all_inventory_items(session)

@app.get("/manage-inventory/{item_id}", response_model=InventoryItem)
def single_inventory_item(item_id: int, session: Annotated[Session, Depends(get_session)]):
    """ Get a single inventory item by ID"""
    try:
        return get_inventory_item_by_id(inventory_item_id=item_id, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @app.delete("/manage-inventory/{item_id}", response_model=dict)
@app.delete("/manage-inventory/{item_id}", response_model=dict)
def delete_single_inventory_item(item_id: int, session: Annotated[Session, Depends(get_session)]):
    """ Delete a single inventory item by ID"""
    try:
        return delete_inventory_item_by_id(inventory_item_id=item_id, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/manage-inventory/{item_id}", response_model=InventoryItem)
def update_inventory_item(item_id: int, inventory: UpdatedInventoryItem, session: Annotated[Session, Depends(get_session)]):
    """ Update a single inventory item by ID"""
    try:
        return update_inventory_item_by_id(inventory_item_id=item_id, to_update_inventory_data=inventory, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))