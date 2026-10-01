from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from mysite.database.db import SessionLocal
from mysite.database.models import User, Product, Order
from mysite.schemas.order_schema import OrderCreateSchema, OrderStatusUpdateSchema, OrderOutSchema
from mysite.api.auth import get_current_user


order_router = APIRouter(prefix="/orders", tags=["Orders"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@order_router.post("/", response_model=OrderOutSchema)
async def create_order(order: OrderCreateSchema, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == order.product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    order_data = Order(
        product_id=order.product_id,
        user_id=current_user.id
    )

    db.add(order_data)
    db.commit()
    db.refresh(order_data)

    return order_data


@order_router.get("/", response_model=list[OrderOutSchema])
async def get_orders(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()

    return orders


@order_router.get("/{order_id}", response_model=OrderOutSchema)
async def get_order(order_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


@order_router.put("/{order_id}", response_model=OrderOutSchema)
async def update_order(order_id: int, order_data: OrderStatusUpdateSchema, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")

    product = db.query(Product).filter(Product.id == order_data.product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Продукт не найден")

    order.product_id = order_data.product_id
    order.status = order_data.status

    db.commit()
    db.refresh(order)

    return order


@order_router.delete("/{order_id}")
async def delete_order(order_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)
    db.commit()

    return {"message": "Order успешно удален"}