from db.base_class import Base 
from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, Text, Boolean, DateTime 
from sqlalchemy.orm import relationship



class Blog(Base):
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True, index=True)
    content = Column(Text, nullable=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=False)
    
    # author = relationship("User", back_populates="blogs")


