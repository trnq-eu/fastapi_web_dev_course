from database import Base
from sqlalchemy import Column, Integer, String, Boolean


class Post(Base):
    __tablename__='posts'
    __allow_unmapped__ = True # inserito successivamente
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)
    