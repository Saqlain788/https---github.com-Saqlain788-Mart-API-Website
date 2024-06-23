from app.models.product_model import Product, updatedproduct
from sqlmodel import Session, select  
from fastapi import HTTPException 

# Add a New Product to the Database
def add_new_product(product_data:Product, session:Session):
    session.add(product_data)
    session.commit()
    session.refresh(product_data)
    return product_data

# Get All Produts from the DB.
def get_all_products(session:Session):
    all_products = session.exec(select(Product)).all()
    return all_products

# Get a Product by ID
def get_product_by_id(product_id:int, session:Session):
    product = session.exec(select(Product).where(Product.id == product_id)).one_or_none() 
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Delete Product by ID
def delete_product_by_id(product_id:int, session:Session):
    product = session.exec(select(Product).where(Product.id == product_id)).one_or_none() 
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()
    return {'message': "Product deleted successfully"}

# Update Product by ID
def update_product_by_id(product_id: int, to_update_product_data:updatedproduct, session: Session):
    # Step 1: Get the Product by ID
    product = session.exec(select(Product).where(Product.id == product_id)).one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    # Step 2: Update the Product
    hero_data = to_update_product_data.model_dump(exclude_unset=True)
    product.sqlmodel_update(hero_data)
    session.add(product)
    session.commit()
    return product

def validate_product_id(product_id:int, session:Session) -> Product | None:
    product = session.exec(select(Product).where(Product.id == product_id)).one_or_none()   
    return product