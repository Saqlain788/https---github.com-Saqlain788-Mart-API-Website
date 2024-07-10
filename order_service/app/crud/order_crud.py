from sqlmodel import Session, select
from fastapi import HTTPException
from app.models.order_model import Order, UpdatedOrder

# Add a new order to the database
def add_new_order(order: Order, session: Session):
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

# Get all orders from the database
def get_all_orders(session: Session):
    all_orders = session.exec(select(Order)).all()
    print("get_all_orders: Retrieved orders:", all_orders)  # Debugging line
    return all_orders

# Get an order by ID
def get_order_by_id(order_id: int, session: Session):
    order = session.exec(select(Order).where(Order.id == order_id)).one_or_none()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# Delete an order by ID
def delete_order_by_id(order_id: int, session: Session) -> dict:
    order = session.exec(select(Order).where(Order.id == order_id)).one_or_none()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    session.delete(order)
    session.commit()
    return {'message': "Order deleted successfully"}

# Update an order by ID
def update_order_by_id(order_id: int, to_update_order_data: UpdatedOrder, session: Session) -> Order:
    # Get the order from the database
    order = session.exec(select(Order).where(Order.id == order_id)).one_or_none()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    # Update the order with the new data
    update_data = to_update_order_data.dict(exclude_unset=True)
    order.sqlmodel_update(update_data)
    session.add(order)
    session.commit()
    return order

def validate_order_id(order_id:int, session:Session) -> Order | None:
    order = session.exec(select(Order).where(Order.id == order_id)).one_or_none()   
    return order