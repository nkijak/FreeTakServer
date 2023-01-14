#######################################################
#
# uid.py
# Python implementation of the Class uid
# Generated by Enterprise Architect
# Created on:      28-Sep-2020 10:48:30 PM
# Original author: natha
#
#######################################################
from sqlalchemy import Column, ForeignKey
from FreeTAKServer.model.SQLAlchemy.Root import Base
from sqlalchemy import String
from sqlalchemy.orm import relationship


class Uid(Base):
    # default constructor  def __init__(self):
    __tablename__ = "Uid"
    PrimaryKey = Column(ForeignKey("Detail.PrimaryKey"), primary_key=True)
    Detail = relationship("Detail", back_populates="uid")
    # TBD, maybe from Android?
    Droid = Column(String(100))
    version = Column(String(100))
