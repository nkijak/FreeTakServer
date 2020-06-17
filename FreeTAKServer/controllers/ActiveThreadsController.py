#######################################################
# 
# ActiveThreadsController.py
# Python implementation of the Class ActiveThreadsController
# Generated by Enterprise Architect
# Created on:      21-May-2020 9:23:03 AM
# Original author: Natha Paquette
#
#######################################################
from model.ActiveThreads import ActiveThreads

class ActiveThreadsController:
    def __init__(self):  
        self.m_ActiveThreads = ActiveThreads()

    def addClientThread(self, clientInformation, process):
        processObject = (clientInformation, process)
        self.m_ActiveThreads.ThreadArray.append(processObject)

    def addReceiveConnectionsThread(self, ReceiveConnectionsProcess, process):
        processObject = (ReceiveConnectionsProcess, process)
        self.m_ActiveThreads.ThreadArray.append(processObject)

    def removeClientThread(self, clientInformation):
        for x in self.m_ActiveThreads.ThreadArray:
            if x[0] == clientInformation:
                self.m_ActiveThreads.ThreadArray.remove(x)

    def removeReceiveConnectionProcess(self, ReceiveConnectionsProcess):
        for x in self.m_ActiveThreads.ThreadArray:
            if x[0] == ReceiveConnectionsProcess:
                self.m_ActiveThreads.ThreadArray.remove(x)
