from sqlalchemy import Column, Integer, String, JSON, DateTime, Enum, Float
from app.dao.core.base import Base
import enum
from sqlalchemy.sql import func


class OrderStatusEnum(enum.Enum):
    PENDING = "PENDING"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    IN_PROCESS = "IN_PROCESS"

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, unique=True, index=True)
    items = Column(JSON)
    store_id = Column(String, index=True)
    customer_id = Column(String, index=True)
    store_wa_no = Column(String, index=True)
    order_created = Column(DateTime(timezone=True), server_default=func.now())
    order_status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.PENDING)
    
    # Installment plan fields
    total_amount = Column(Float, default=0.0)
    paid_amount = Column(Float, default=0.0)
    installments = Column(JSON) # List of { "due_date": "YYYY-MM-DD", "amount": 100.0, "status": "PAID" | "PENDING" }
    next_due_date = Column(DateTime(timezone=True), nullable=True)
