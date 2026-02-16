from db.base_class import Base 
from sqlalchemy import Column, String, Integer, Boolean 
from sqlalchemy.orm import relationship


# 14 Jan 26 (timestmp 27:00): We would index on order id
class User(Base):
    # id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_superuser = Column(Boolean(), default=False)
    is_active = Column(Boolean(), default=True)
    username = Column(String(255), unique=True, index=True, nullable=False)

    # blogs = relationship("Blog", back_populates="author ")
