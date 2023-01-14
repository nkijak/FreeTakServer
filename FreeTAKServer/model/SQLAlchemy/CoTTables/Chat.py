#######################################################
#
# chat.py
# Python implementation of the Class chat
# Generated by Enterprise Architect
# Created on:      28-Sep-2020 10:48:13 PM
# Original author: natha
#
#######################################################
from sqlalchemy import Column, ForeignKey
from FreeTAKServer.model.SQLAlchemy.Root import Base
from sqlalchemy.orm import relationship
from sqlalchemy import String


class Chat(Base):
    # default constructor  def __init__(self):
    __tablename__ = "Chat"
    PrimaryKey = Column(ForeignKey("Detail.PrimaryKey"), primary_key=True)
    Detail = relationship("Detail", back_populates="chat")
    # TBD: the callsign of the receiver?
    chatroom = Column(String(100))
    # TBD,
    groupOwner = Column(String(100))
    # TBD: the unique id of the sender?
    id = Column(String(100))
    # the group where thise chat is attached
    parent = Column(String(100))
    # the call sign of the sender
    senderCallsign = Column(String(100))
