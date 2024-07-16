# crud.py
from sqlmodel import Session, select
from fastapi import HTTPException
from app.models.payment_model import Payment, PaymentCreate, PaymentUpdate

def create_payment(payment: PaymentCreate, session: Session):
    db_payment = Payment.from_orm(payment)
    session.add(db_payment)
    session.commit()
    session.refresh(db_payment)
    return db_payment

def get_all_payments(session: Session):
    payments = session.exec(select(Payment)).all()
    return payments

def get_payment_by_id(payment_id: int, session: Session):
    payment = session.exec(select(Payment).where(Payment.id == payment_id)).one_or_none()
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

def update_payment_by_id(payment_id: int, to_update_payment_data: PaymentUpdate, session: Session):
    payment = session.exec(select(Payment).where(Payment.id == payment_id)).one_or_none()
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    update_data = to_update_payment_data.dict(exclude_unset=True)
    payment.sqlmodel_update(update_data)
    session.add(payment)
    session.commit()
    return payment

def delete_payment_by_id(payment_id: int, session: Session):
    payment = session.exec(select(Payment).where(Payment.id == payment_id)).one_or_none()
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    session.delete(payment)
    session.commit()
    return {'message': "Payment deleted successfully"}

def validate_payment_id(payment_id:int, session:Session) -> Payment | None:
    payment = session.exec(select(Payment).where(Payment.id == payment_id)).one_or_none()    
    return payment