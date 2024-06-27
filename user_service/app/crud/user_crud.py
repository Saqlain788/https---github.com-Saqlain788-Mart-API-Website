# crud.py
from sqlmodel import Session, select
from fastapi import HTTPException
from app.models.user_model import User, UserUpdate, UserCreate

def create_user(user: UserCreate, session: Session):
    db_user = User.from_orm(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def get_all_users(session: Session):
    all_users = session.exec(select(User)).all() 
    return all_users

def get_user_by_id(user_id: int, session: Session):
    user = session.exec(select(User).where(User.id == user_id)).one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def delete_user_by_id(user_id: int, session: Session):
    user = session.exec(select(User).where(User.id == user_id)).one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"message": "User deleted successfully"}


def update_user_by_id(user_id: int, user_update: UserUpdate, session: Session):
    user = session.exec(select(User).where(User.id == user_id)).one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = user_update.dict(exclude_unset=True)
    user.sqlmodel_update(update_data)
    session.add(user)
    session.commit()
    return user

