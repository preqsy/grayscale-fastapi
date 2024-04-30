from sqlalchemy import Column, Integer, LargeBinary, String
from database import Base

class Picture(Base):
    __tablename__ = "pictures"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    picture = Column(LargeBinary)