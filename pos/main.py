from fastapi import FastAPI
from database import Base,engine

from routers.category_router import router as category_router
from routers.product_router import router as product_router
from routers.supplier_router import router as supplier_router
from routers.customer_router import router as customer_router
from routers.user_router import router as user_router
from routers.sale_router import router as sale_router
from routers.sale_item_router import router as sale_item_router
from routers.payment_router import router as payment_router
from routers.receipt_router import router as receipt_router

Base.metadata.create_all(bind=engine)
app=FastAPI(title="POS API", version="1")


app.include_router(category_router)

app.include_router(product_router)

app.include_router(supplier_router)

app.include_router(customer_router)

app.include_router(user_router)

app.include_router(sale_router)

app.include_router(sale_item_router)

app.include_router(payment_router)

app.include_router(receipt_router)