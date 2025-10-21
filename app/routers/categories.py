from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from app.schemas.category import CategoryCreate, CategoryResponse
from app.models import User
from app.dependencies import get_current_active_user
from app.models import Category
from app.dependencies import get_db

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=Dict[str, List[CategoryResponse]])
def get_categories(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    categories = db.query(Category).filter(Category.user_id == current_user.id).all()
    if categories is None:
        raise HTTPException(status_code=404, detail="There are no categories")
    return {"categories": categories}


@router.get("/{category_id}", response_model=CategoryResponse)
def get_categories(category_id: int, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id, Category.user_id == current_user.id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("", response_model=CategoryResponse)
def create_category(category: CategoryCreate, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    new_category = Category(
        name=category.name,
        user_id=current_user.id
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, new_category: CategoryCreate, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id, Category.user_id == current_user.id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category.name = new_category.name
    db.commit()
    db.refresh(category)
    return category


@router.delete('/{category_id}')
def delete_category(category_id: int, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id, Category.user_id == current_user.id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"message": "Category deleted"}