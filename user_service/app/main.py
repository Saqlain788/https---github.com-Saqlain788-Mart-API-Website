# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, SQLModel
from aiokafka import AIOKafkaProducer

# import json
from app import user_pb2
import asyncio
from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator

from app.models.user_model import User, UserUpdate, UserCreate
from app.db import get_session, engine
from app.crud.user_crud import  get_user_by_id, update_user_by_id, delete_user_by_id, get_all_users
from app.consumer.user_add_consumer import consume_message
from app.producer import get_kafka_producer

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Creating tables...")

    task = asyncio.create_task(consume_message("orderplaced", "broker:19092"))
    create_db_and_tables()
    try:
        yield
    finally:
        task.cancel()
        await task

app = FastAPI(lifespan=lifespan, title="User Service API", version="0.0.1")

@app.post("/users/", response_model=User)
async def create_new_user(user: UserCreate, 
                          session: Annotated[Session, Depends(get_session)], 
                          producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    
    # user_dict = {field: getattr(user, field) for field in user.dict()}
    # user_json = json.dumps(user_dict).encode("utf-8")
    # print("USER JSON", user_json)
    # await producer.send_and_wait("UserCreated", user_json)
    # return user
# through protobuf
    user_protobuf = user_pb2.UserCreate(order_id=user.order_id, name=user.name, email=user.email, password=user.password)
    print(f"User Protobuf: {user_protobuf}")  # Debugging line
    serialized_user = user_protobuf.SerializeToString()
    print(f"Serialized User: {serialized_user}")  # Debugging line
    await producer.send_and_wait("UserCreated", serialized_user)
    return user
@app.get("/users/all", response_model=list[User])
def get_all_users_from_DB(session: Annotated[Session, Depends(get_session)]):
    users = get_all_users(session)
    return users

@app.get("/users/{user_id}", response_model=User)
def get_single_user_by_id(user_id: int, session: Annotated[Session, Depends(get_session)]):
    try:
        return get_user_by_id(user_id=user_id, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    

@app.delete("/users/{user_id}", response_model=dict)
def delete_single_user(user_id: int, session: Annotated[Session, Depends(get_session)]):
    try:
        return delete_user_by_id(user_id=user_id, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    
@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate, session: Annotated[Session, Depends(get_session)]):
    try:
        return update_user_by_id(user_id=user_id, user_update=user, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e