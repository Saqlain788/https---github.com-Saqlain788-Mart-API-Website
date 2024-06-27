# crud.py
from sqlmodel import Session, select
from fastapi import HTTPException
from app.models.notification_model import Notification, NotificationCreate, NotificationUpdate

def create_notification(notification: NotificationCreate, session: Session) -> Notification:
    db_notification = Notification.from_orm(notification)
    session.add(db_notification)
    session.commit()
    session.refresh(db_notification)
    return db_notification

def get_notification_by_id(notification_id: int, session: Session) -> Notification:
    statement = select(Notification).where(Notification.id == notification_id)
    return session.exec(statement).one_or_none()

def update_notification_by_id(notification_id: int, notification_update: NotificationUpdate, session: Session) -> Notification:
    db_notification = session.get(Notification, notification_id)
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    update_data = notification_update.dict(exclude_unset=True)
    db_notification.sqlmodel_update(update_data)
    session.add(db_notification)
    session.commit()
    session.refresh(db_notification)
    return db_notification

def delete_notification_by_id(notification_id: int, session: Session) -> bool:
    db_notification = session.get(Notification, notification_id)
    if not db_notification:
        return False
    session.delete(db_notification)
    session.commit()
    return True
