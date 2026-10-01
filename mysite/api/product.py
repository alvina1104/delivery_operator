from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from mysite.database.db import SessionLocal
from mysite.database.models import Product
from mysite.schemas.product_schema import ProductCreateSchema, ProductUpdateSchema, ProductOutSchema


product_router = APIRouter(prefix="/products", tags=["Products"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@product_router.post("/", response_model=ProductOutSchema)
async def create_product(product: ProductCreateSchema, db: Session = Depends(get_db)):
    product_data = Product(
        category=product.category,
        store=product.store,
        product_name=product.product_name,
        price=product.price
    )

    db.add(product_data)
    db.commit()
    db.refresh(product_data)

    return product_data


@product_router.get("/", response_model=list[ProductOutSchema])
async def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()

    return products


@product_router.get("/{product_id}", response_model=ProductOutSchema)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@product_router.put("/{product_id}", response_model=ProductOutSchema)
async def update_product(product_id: int, product: ProductUpdateSchema, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()

    if not product_db:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(product_db, key, value)

    db.commit()
    db.refresh(product_db)

    return product_db


@product_router.delete("/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()

    return {"message": "Product успешно удален"}