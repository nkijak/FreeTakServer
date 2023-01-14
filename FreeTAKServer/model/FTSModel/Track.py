from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject

#######################################################
#
# Track.py
# Python implementation of the Class Track
# Generated by Enterprise Architect
# Created on(FTSProtocolObject):      11-Feb-2020 11(FTSProtocolObject):08(FTSProtocolObject):09 AM
# Original author: Corvo
#
#######################################################
from FreeTAKServer.model.FTSModelVariables.TrackVariables import TrackVariables as vars


class Track(FTSProtocolObject):
    def __init__(self):
        self.course = None
        self.speed = None
        self.slope = None

    @staticmethod
    def connection(
        COURSE=vars.connection().COURSE,
        SPEED=vars.connection().SPEED,
        SLOPE=vars.connection().SLOPE,
    ):
        track = Track()
        track.setcourse(COURSE)
        track.setspeed(SPEED)
        track.setslope(SLOPE)
        return track

    @staticmethod
    def UserUpdate(
        SPEED=vars.UserUpdate().speed,
        COURSE=vars.UserUpdate().course,
        SLOPE=vars.UserUpdate().SLOPE,
    ):
        track = Track()
        track.setspeed(SPEED)
        track.setcourse(COURSE)
        track.setslope(SLOPE)
        return track

    @staticmethod
    def DroneSensor(
        COURSE=vars.DroneSensor().COURSE,
        SPEED=vars.DroneSensor().SPEED,
        SLOPE=vars.DroneSensor().SLOPE,
    ):
        track = Track()
        track.setcourse(COURSE)
        track.setspeed(SPEED)
        track.setslope(SLOPE)
        return track

    # speed getter
    def getspeed(self):
        return self.speed

    # speed setter
    def setspeed(self, speed=0):
        self.speed = speed

    # course getter
    def getcourse(self):
        return self.course

    # course setter
    def setcourse(self, course=0):
        self.course = course

    def setslope(self, slope):
        self.slope = slope

    def getslope(self):
        return self.slope
