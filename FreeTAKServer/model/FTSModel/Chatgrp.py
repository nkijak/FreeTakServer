from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject

#######################################################
#
# chatgrp.py
# Python implementation of the Class chatgrp
# Generated by Enterprise Architect
# Created on(FTSProtocolObject):      11-Feb-2020 11(FTSProtocolObject):08(FTSProtocolObject):10 AM
# Original author: Corvo
#
#######################################################
from FreeTAKServer.model.FTSModelVariables.ChatgrpVariables import (
    ChatgrpVariables as vars,
)


class Chatgrp(FTSProtocolObject):
    def __init__(self):
        self.uid0 = None
        self.uid1 = None
        self.id = None

    @staticmethod
    def geochat(
        uid0=vars.geochat().UID0, uid1=vars.geochat().UID1, id=vars.geochat().ID
    ):
        chatgrp = Chatgrp()
        chatgrp.setid(id)
        chatgrp.setuid0(uid0)
        chatgrp.setuid1(uid1)
        return chatgrp

    def chatToTeamFunc(self, uid0, uid1, id):  # noqa
        self.setuid0(uid0)
        self.setuid1(uid1)
        self.setid(id)

    def chatToGroupFunc(self, uid0, uid1, id):  # noqa
        self.chatToTeamFunc(uid0, uid1, id)

    def chatToAllFunc(self, uid0, uid1, id):  # noqa
        self.chatToTeamFunc(uid0, uid1, id)

    def getuid0(self):
        return self.uid0

    # uid0 setter
    def setuid0(self, uid0=0):
        self.uid0 = uid0

    # uid1 getter
    def getuid1(self):
        return self.uid1

    # uid1 setter
    def setuid1(self, uid1=0):
        self.uid1 = uid1

    # id getter
    def getid(self):
        return self.id

    # id setter
    def setid(self, id=0):
        self.id = id
