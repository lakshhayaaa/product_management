from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()

class Product(Base):
  
  __tablename__='product'

  id=Column(Integer,primary_key=True,index=True)
  name=Column(String,nullable=False)
  price=Column(Float,nullable=False)
  quantity=Column(Integer,nullable=False)
  description=Column(String,nullable=True)