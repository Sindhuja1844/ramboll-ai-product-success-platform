from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    launch_date = Column(Date)
    owning_team = Column(String)


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


class Usage(Base):
    __tablename__ = "usage"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
    date = Column(Date)
    active_users = Column(Integer)
    sessions = Column(Integer)
    feature_events = Column(Integer)


class Cost(Base):
    __tablename__ = "costs"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
    date = Column(Date)
    compute_cost = Column(Float)
    token_cost = Column(Float)