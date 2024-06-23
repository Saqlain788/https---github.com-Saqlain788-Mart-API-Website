from app.models.inventory_model import InventoryItem, UpdatedInventoryItem
from sqlmodel import Session, select  
from fastapi import HTTPException 

# Add a New Product to the Database
def add_new_inventory_item(inventory_item:InventoryItem, session:Session):
    session.add(inventory_item)
    session.commit()
    session.refresh(inventory_item)
    return inventory_item

# Get All Produts from the DB.
def get_all_inventory_items(session:Session):
    all_inventories = session.exec(select(InventoryItem)).all()
    return all_inventories

# Get a Product by ID
def get_inventory_item_by_id(inventory_item_id:int, session:Session):
    inventory_item = session.exec(select(InventoryItem).where(InventoryItem.id == inventory_item_id)).one_or_none() 
    if inventory_item is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory_item

# Delete Product by ID
def delete_inventory_item_by_id(inventory_item_id:int, session:Session):
    inventory_item = session.exec(select(InventoryItem).where(InventoryItem.id == inventory_item_id)).one_or_none() 
    if inventory_item is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    session.delete(inventory_item)
    session.commit()
    return {'message': "Inventory deleted successfully"}

# Update Product by ID
def update_inventory_item_by_id(inventory_item_id:int, to_update_inventory_data:UpdatedInventoryItem, session:Session):
    inventory_item = session.exec(select(InventoryItem).where(InventoryItem.id == inventory_item_id)).one_or_none()
    if inventory_item is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    update_data = to_update_inventory_data.dict(exclude_unset=True)
    inventory_item.sqlmodel_update(update_data)
    session.add(inventory_item)
    session.commit()
    session.refresh(inventory_item)
    return inventory_item