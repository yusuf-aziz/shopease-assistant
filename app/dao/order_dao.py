from app.dao.core.session import SessionLocal, engine
from app.models.order import Order, OrderStatusEnum
from app.dao.core.base import Base
from datetime import datetime
import json


# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

def save_order(items, store_id=None, customer_id=None, store_wa_no=None, total_amount=0.0, paid_amount=0.0, installments=None, next_due_date=None):
    session = SessionLocal()
    last_order = session.query(Order).order_by(Order.id.desc()).first()
    next_id = last_order.id + 1 if last_order else 1
    order_id = f"ORD-{next_id}"

    order = Order(
        order_id=order_id,
        items=items,
        store_id=store_id,
        customer_id=customer_id,
        store_wa_no=store_wa_no,
        order_created=datetime.now(),
        order_status=OrderStatusEnum.PENDING,
        total_amount=total_amount,
        paid_amount=paid_amount,
        installments=installments,
        next_due_date=next_due_date
    )
    session.add(order)
    session.commit()
    session.close()
    return order_id

def get_order(order_id):
    session = SessionLocal()
    order = session.query(Order).filter_by(order_id=order_id).first()
    session.close()
    if order:
        return order
    return None

def get_orders_by_customer(customer_id):
    session = SessionLocal()
    try:
        return session.query(Order).filter(Order.customer_id == customer_id).order_by(Order.order_created.desc()).limit(5).all()
    finally:
        session.close()
