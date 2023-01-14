#######################################################
#
# Detail.py
# Python implementation of the Class Detail
# Generated by Enterprise Architect
# Created on:      26-Sep-2020 9:41:25 PM
# Original author: natha
#
#######################################################
from sqlalchemy import Column, ForeignKey
from FreeTAKServer.model.SQLAlchemy.Root import Base
from sqlalchemy import String
from sqlalchemy.orm import relationship
import FreeTAKServer.model.SQLAlchemy.CoTTables.Archive
import FreeTAKServer.model.SQLAlchemy.CoTTables._Group
import FreeTAKServer.model.SQLAlchemy.CoTTables.Chat
import FreeTAKServer.model.SQLAlchemy.CoTTables.Color
import FreeTAKServer.model.SQLAlchemy.CoTTables.Contact
import FreeTAKServer.model.SQLAlchemy.CoTTables.Dest
import FreeTAKServer.model.SQLAlchemy.CoTTables.Emergency
import FreeTAKServer.model.SQLAlchemy.CoTTables.Link
import FreeTAKServer.model.SQLAlchemy.CoTTables.Marti
import FreeTAKServer.model.SQLAlchemy.CoTTables.Precisionlocation
import FreeTAKServer.model.SQLAlchemy.CoTTables.Remarks
import FreeTAKServer.model.SQLAlchemy.CoTTables.Serverdestination
import FreeTAKServer.model.SQLAlchemy.CoTTables.Status
import FreeTAKServer.model.SQLAlchemy.CoTTables.Summary
import FreeTAKServer.model.SQLAlchemy.CoTTables.Takv
import FreeTAKServer.model.SQLAlchemy.CoTTables.Track
import FreeTAKServer.model.SQLAlchemy.CoTTables.Uid
import FreeTAKServer.model.SQLAlchemy.CoTTables.Usericon
import FreeTAKServer.model.SQLAlchemy.CoTTables._Video
import FreeTAKServer.model.SQLAlchemy.CoTTables.ConnectionEntry
import FreeTAKServer.model.SQLAlchemy.CoTTables.Sensor

ALLDELETE = "all, delete"


class Detail(Base):
    __tablename__ = "Detail"
    PrimaryKey = Column(ForeignKey("Event.uid"), primary_key=True)
    xmlString = Column(String(100))
    archive = relationship("Archive", uselist=False, cascade=ALLDELETE)
    _group = relationship(
        "_Group", uselist=False, back_populates="Detail", cascade=ALLDELETE
    )
    chat = relationship("Chat", uselist=False, cascade=ALLDELETE)
    color = relationship("Color", uselist=False, cascade=ALLDELETE)
    contact = relationship(
        "Contact", back_populates="Detail", uselist=False, cascade=ALLDELETE
    )
    emergency = relationship("Emergency", uselist=False, cascade=ALLDELETE)
    link = relationship(
        "Link", back_populates="Detail", uselist=False, cascade=ALLDELETE
    )
    marti = relationship("Marti", uselist=False, cascade=ALLDELETE)
    precisionlocation = relationship(
        "Precisionlocation", uselist=False, cascade=ALLDELETE
    )
    remarks = relationship("Remarks", uselist=False, cascade=ALLDELETE)
    serverdestination = relationship(
        "Serverdestination", uselist=False, cascade=ALLDELETE
    )
    status = relationship("Status", uselist=False, cascade=ALLDELETE)
    summary = relationship(
        "Summary", back_populates="Detail", uselist=False, cascade=ALLDELETE
    )
    takv = relationship("Takv", uselist=False, cascade=ALLDELETE)
    track = relationship("Track", uselist=False, cascade=ALLDELETE)
    uid = relationship("Uid", uselist=False, cascade=ALLDELETE)
    usericon = relationship("Usericon", uselist=False, cascade=ALLDELETE)
    _video = relationship("_Video", uselist=False, cascade=ALLDELETE)
    sensor = relationship("Sensor", uselist=False, cascade=ALLDELETE)
