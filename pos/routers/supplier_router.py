from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.supplier import SupplierCreate, SupplierUpdate, SupplierResponse
from services.supplier_service import supplier_service


router = APIRouter(prefix="/suppliers", tags=["Suppliers"])


@router.get("/", response_model=list[SupplierResponse], status_code=status.HTTP_200_OK)
def get_suppliers(db: Session = Depends(get_db)):
    return supplier_service.list_suppliers(db)


@router.get("/{supplier_id}", response_model=SupplierResponse, status_code=status.HTTP_200_OK)
def get_supplier(supplier_id: UUID, db: Session = Depends(get_db)):
    return supplier_service.get_supplier(db, supplier_id)


@router.post("/", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_supplier(data: SupplierCreate, db: Session = Depends(get_db)):
    return supplier_service.create_supplier(db, data)


@router.put("/{supplier_id}", response_model=SupplierResponse, status_code=status.HTTP_200_OK)
def update_supplier(supplier_id: UUID, data: SupplierUpdate, db: Session = Depends(get_db)):
    return supplier_service.update_supplier(db, supplier_id, data)


@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(supplier_id: UUID, db: Session = Depends(get_db)):
    supplier_service.delete_supplier(db, supplier_id)