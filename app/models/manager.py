from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Manager(Base):
    __tablename__ = 'managers'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # 員工ID
    manager_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # 上司ID

    user = relationship('User', foreign_keys=[user_id], back_populates='subordinate_relations')
    manager = relationship('User', foreign_keys=[manager_id], back_populates='manager_relations')
