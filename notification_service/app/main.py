# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, SQLModel
from aiokafka import AIOKafkaProducer
import json
import asyncio
from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator

from app.models.notification_model import Notification, NotificationCreate, NotificationUpdate
from app.db import get_session, engine
from app.crud.notification_crud import create_notification, get_notification_by_id, update_notification_by_id, delete_notification_by_id
from app.consumer.notification_consumer import consume_message
from app.producer import get_kafka_producer

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Creating tables...")
    create_db_and_tables()

    task = asyncio.create_task(consume_message("NotificationCreated", "broker:19092"))
    try:
        yield
    finally:
        task.cancel()
        await task

app = FastAPI(lifespan=lifespan, title="Notification Service API", version="0.0.1")

@app.post("/notifications/", response_model=Notification)
async def get_notification(notification: NotificationCreate, session: Annotated[Session, Depends(get_session)], producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    # db_notification = create_notification(notification, session)
    notification_dict = {field: getattr(notification, field) for field in notification.dict()}
    notification_json = json.dumps(notification_dict).encode("utf-8")
    await producer.send_and_wait("NotificationCreated", notification_json)
    return notification

@app.get("/notifications/{notification_id}", response_model=Notification)
def read_notification(notification_id: int, session: Annotated[Session, Depends(get_session)]):
    db_notification = get_notification_by_id(notification_id, session)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return db_notification

@app.put("/notifications/{notification_id}", response_model=Notification)
def update_notification(notification_id: int, notification: NotificationUpdate, session: Annotated[Session, Depends(get_session)]):
    db_notification = update_notification_by_id(notification_id, notification, session)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return db_notification

@app.delete("/notifications/{notification_id}", response_model=dict)
def delete_notification(notification_id: int, session: Annotated[Session, Depends(get_session)]):
    result = delete_notification_by_id(notification_id, session)
    if not result:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"message": "Notification deleted successfully"}
