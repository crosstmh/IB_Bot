from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from Singleton import *

engine = create_engine('sqlite:///Data/data.sqlite', echo = True)
Base = declarative_base()


class OrderModel(Base):
    __tablename__ = 'Orders'

    id = Column(Integer, primary_key=True)
    con_id = Column(Integer, nullable=False, index=True)
    position = Column(Integer, nullable=False, default=0)
    avg_cost = Column(Double, nullable=False, default=0.0)
    secType = Column(String, default="OPT")
    right = Column(String, default="C")
    symbol = Column(String,default="TSLA")
    strike = Column(Double,nullable=False)
    lastTradeDate = Column(String)
    tradingClass = Column(String)
    trade_id = Column(Integer,index=True)
    createtime = Column(String)
    action = Column(String)
    is_open = Column(Integer, default=1)


class TradeModel(Base):
    __tablename__ = 'Trades'

    id = Column(Integer, primary_key=True)
    stock_leg_con_id = Column(Integer, nullable=False)
    leg1_con_id = Column(Integer, nullable=False)
    leg2_con_id = Column(Integer, nullable=False)
    leg3_con_id = Column(Integer, nullable=False)
    leg4_con_id = Column(Integer, nullable=False)
    createtime = Column(String)
    is_open = Column(Integer, default=1)


class ORMHelper(metaclass=Singleton):
    session = sessionmaker(bind=engine)()

