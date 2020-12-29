from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, text, String

from app import db


class OrderModel(db.Model):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    status = Column(Integer, nullable=False)
    total_price = Column(Integer, nullable=False)
    payment_method = Column(String(100), nullable=False)
    payment_status = Column(String(100), nullable=False)
    va = Column(String(100))
    deeplink = Column(String(255))
    qr_code = Column(String(255))
    transaction_fee = Column(Integer, nullable=False)
    created_at = Column(
        DateTime, default=datetime.now,
        server_default=text('CURRENT_TIMESTAMP')
    )
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP')
    )
