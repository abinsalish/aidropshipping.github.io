from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
# In a real app, you would import the get_current_user dependency here
# import firebase_admin.firestore as firestore
from .auth import get_current_user

router = APIRouter()

# Schema
class Product(BaseModel):
    id: Optional[str] = None
    name: str
    status: str = "draft"
    aiAnalyticsScore: int = 0
    supplier: str

# In-memory mock database until Firestore is hooked up
mock_database = []
product_id_counter = 1

@router.get("/", response_model=List[Product])
async def list_products(user: dict = Depends(get_current_user)):
    """List dropshipping products for the user (mocked right now)"""
    return mock_database

@router.post("/", response_model=Product)
async def create_product(product: Product, user: dict = Depends(get_current_user)):
    global product_id_counter
    product.id = str(product_id_counter)
    product_id_counter += 1
    mock_database.append(product)
    return product

@router.delete("/{product_id}")
async def delete_product(product_id: str, user: dict = Depends(get_current_user)):
    global mock_database
    prod = next((p for p in mock_database if p.id == product_id), None)
    if not prod:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    mock_database = [p for p in mock_database if p.id != product_id]
    return {"message": "Product deleted successfully"}
