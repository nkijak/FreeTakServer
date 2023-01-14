#######################################################
#
# FederationClientService.py
# Python implementation of the Class FederationClientService
# Generated by Enterprise Architect
# Created on:      29-Dec-2020 8:10:38 AM
# Original author: natha
#
#######################################################
import selectors
import socket
import ssl
import threading
from typing import Dict, List, Tuple

from FreeTAKServer.core.configuration.CreateLoggerController import (
    CreateLoggerController,
)
from FreeTAKServer.core.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.core.configuration.MainConfig import MainConfig
from FreeTAKServer.core.persistence.DatabaseController import DatabaseController
from FreeTAKServer.core.services.federation.external_data_handlers import (
    FederationProtobufConnectionHandler,
    FederationProtobufDisconnectionHandler,
    FederationProtobufStandardHandler,
    FederationProtobufValidationHandler,
)
from FreeTAKServer.core.services.federation.federation_service_base import (
    FederationServiceBase,
)
from FreeTAKServer.core.services.federation.handlers import (
    ConnectHandler,
    DataValidationHandler,
    DestinationValidationHandler,
    DisconnectHandler,
    HandlerBase,
    SendConnectionDataHandler,
    SendDataHandler,
    SendDisconnectionDataHandler,
    StopHandler,
)
from FreeTAKServer.model.ClientInformation import ClientInformation
from FreeTAKServer.model.federate import Federate
from FreeTAKServer.model.protobufModel.fig_pb2 import FederatedEvent
from FreeTAKServer.model.SpecificCoT.SpecificCoTAbstract import SpecificCoTAbstract

# Make a connection to the MainConfig object for all routines below
config = MainConfig.instance()

loggingConstants = LoggingConstants(log_name="FTS_FederationClientService")
logger = CreateLoggerController(
    "FTS_FederationClientService", logging_constants=loggingConstants
).getLogger()

loggingConstants = LoggingConstants()


class FederationClientServiceController(FederationServiceBase):
    """A service which controllers the connection too and transfer of data with
    federated servers.
    """

    def __init__(self):
        self.logger = logger
        self._define_command_responsibility_chain()
        self._define_connection_responsibility_chain()
        self._define_service_responsibility_chain()
        self._define_external_data_responsibility_chain()
        self._define_data_responsibility_chain()
        self.pipe = None
        self.federates: Dict[str, Federate] = {}
        self.sel = selectors.DefaultSelector()
        self.user_dict = {}

    def get_service_users(self) -> List[FederatedEvent]:
        return self.user_dict.values()

    def add_service_user(self, user: FederatedEvent) -> None:
        """add a service user to this services user persistence mechanism

        Returns: None

        """
        self.user_dict[user.contact.uid] = user

    def remove_service_user(self, user: FederatedEvent):
        """remove a service user from this services user persistence mechanism

        Returns: None

        """
        del self.user_dict[user.contact.uid]

    def define_responsibility_chain(self):
        pass

    def _create_context(self):
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.context.load_cert_chain(
            config.federationCert,
            config.federationKey,
            password=config.federationKeyPassword,
        )
        self.context.set_ciphers("DEFAULT@SECLEVEL=1")

    def _define_external_data_responsibility_chain(self):
        """this method is responsible for defining the responsibility chain which handles external data
        eg. data sent to FTS by a federate

        Returns:

        """
        fed_proto_standard_handler = FederationProtobufStandardHandler()

        fed_proto_disconnect_handler = FederationProtobufDisconnectionHandler()
        fed_proto_disconnect_handler.setNextHandler(fed_proto_standard_handler)

        fed_proto_connection_handler = FederationProtobufConnectionHandler()
        fed_proto_connection_handler.setNextHandler(fed_proto_disconnect_handler)

        fed_proto_validation_handler = FederationProtobufValidationHandler()
        fed_proto_validation_handler.setNextHandler(fed_proto_connection_handler)

        self.external_data_chain = fed_proto_validation_handler

    def _call_responsibility_chain(self, command):
        """this method is responsible for calling the responsibility chains for all command types:
            service level commands; start, stop etc
            Connection level commands; close connection, open connection etc
            data level commands; send data x, each handler is responsible for some facet of data validation before
                the connection receives it

        Returns: output from successful handler

        """
        # if command.level == "SERVICE":
        if command == "STOP":
            self.service_chain.Handle(obj=self, command=command)

        # elif command.level == "CONNECTION":
        elif isinstance(command, tuple) and (
            command[1] == "DELETE" or command[1] == "CREATE" or command[1] == "UPDATE"
        ):
            self.connection_chain.Handle(obj=self, command=command)

        # elif command.level == "DATA":
        if isinstance(command, SpecificCoTAbstract) or isinstance(
            command, ClientInformation
        ):
            self.data_chain.Handle(obj=self, command=command)

    def _define_service_responsibility_chain(self):
        """this method is responsible for defining the responsibility chain which will handle service level commands;
            or commands which effect the entire service

        Returns: the entry handler for this responsibility chain

        """
        stop_handler = StopHandler()
        self.service_chain = stop_handler

    def _define_connection_responsibility_chain(self):
        """this method is responsible for defining the responsibility chain which will handle connection level commands;
            or commands which effect the status of a connection at the socket level

        Returns: the entry handler for this responsibility chain

        """
        connect_handler = ConnectHandler()
        disconnect_handler = DisconnectHandler()
        disconnect_handler.setNextHandler(connect_handler)
        self.connection_chain = disconnect_handler

    def _define_data_responsibility_chain(self):
        """this method is responsible for defining the responsibility chain which will handle data level commands;
            or commands which transfer data to a client

        Returns: the entry handler for this responsibility chain

        """

        send_data_handler = SendDataHandler()

        destination_validation_handler = DestinationValidationHandler()
        destination_validation_handler.setNextHandler(send_data_handler)

        send_disconnection_data_handler = SendDisconnectionDataHandler()
        send_disconnection_data_handler.setNextHandler(destination_validation_handler)

        send_connection_data_handler = SendConnectionDataHandler()
        send_connection_data_handler.setNextHandler(send_disconnection_data_handler)

        data_validation_handler = DataValidationHandler()
        data_validation_handler.setNextHandler(send_connection_data_handler)

        self.data_chain = data_validation_handler

    def _define_command_responsibility_chain(self) -> HandlerBase:
        self.m_StopHandler = StopHandler()

        self.m_ConnectHandler = ConnectHandler()
        self.m_ConnectHandler.setNextHandler(self.m_StopHandler)

        self.m_DisconnectHandler = DisconnectHandler()
        self.m_DisconnectHandler.setNextHandler(self.m_ConnectHandler)

        self.m_SendDataHandler = SendDataHandler()
        self.m_SendDataHandler.setNextHandler(self.m_DisconnectHandler)

        self.m_SendDisconnectionHandler = SendDisconnectionDataHandler()
        self.m_SendDisconnectionHandler.setNextHandler(self.m_SendDataHandler)

        # first handler in chain of responsibility and should be called first
        self.m_SendConnectionHandler = SendConnectionDataHandler()
        self.m_SendConnectionHandler.setNextHandler(self.m_SendDisconnectionHandler)

    def main(self):
        inbound_data_thread = threading.Thread(target=self.inbound_data_handler)
        inbound_data_thread.start()
        outbound_data_thread = threading.Thread(target=self.outbound_data_handler)
        outbound_data_thread.start()
        inbound_data_thread.join()

    def serialize_data(self, data_object: FederatedEvent):
        specific_obj = self._process_protobuff_to_object(data_object)
        return specific_obj

    def outbound_data_handler(self):
        """this is the main process responsible for receiving data from federates and sharing
        with FTS core

        Returns:

        """
        while True:
            import time

            if self.federates:
                try:
                    data = self.receive_data_from_federate(1)
                except ssl.SSLWantReadError:
                    data = None
                if data:
                    for protobuf_object in data:
                        # TODO: clean all of this up as it's just a PoC

                        # event = etree.Element('event')
                        # SpecificCoTObj = XMLCoTController().categorize_type(protobuf_object.type)
                        try:
                            serialized_data = self.serialize_data(protobuf_object)
                            self.send_command_to_core(serialized_data)
                        except Exception as e:
                            self.logger.warning(
                                "there has been an exception thrown in the outbound_data_handler "
                                + str(e)
                            )
                        """if isinstance(SpecificCoTObj, SendOtherController):
                            detail = protobuf_object.event.other
                            protobuf_object.event.other = ''
                            fts_obj = ProtobufSerializer().from_format_to_fts_object(protobuf_object, Event.Other())
                            protobuf_object.event.other = detail
                            SpecificCoTObj.object = fts_obj
                            SpecificCoTObj.Object =
                        else:
                            fts_obj = ProtobufSerializer().from_format_to_fts_object(protobuf_object, SpecificCoTObj().object)
                            self.pipe.send(data)"""
                else:
                    pass
            else:
                time.sleep(config.MainLoopDelay / 1000)

    def send_command_to_core(self, serialized_data):
        if self.pipe.sender_queue.full():
            print("queue full !!!")
        self.pipe.put(serialized_data)

    def inbound_data_handler(self):
        """this is the main process responsible for receiving data from FTS core

        Returns:

        """
        while True:
            try:
                command = self.pipe.get()
                if command:
                    try:
                        self._call_responsibility_chain(command)
                    except Exception as e:
                        pass

            except Exception as e:
                self.logger.error(str(e))

    def connect_to_server(self, server_vars: Tuple[str, str]) -> None:
        try:
            federate_db_obj = self.db.query_Federation(f'id == "{server_vars[0]}"')[0]
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
            ssock = self.context.wrap_socket(
                sock, server_hostname=federate_db_obj.address
            )
            ssock.settimeout(10)
            ssock.connect((str(federate_db_obj.address), int(federate_db_obj.port)))
            ssock.setblocking(False)
            federate = Federate()
            federate.uid = server_vars[0]
            federate.addr = federate_db_obj.address
            federate.conn = ssock
            federate.name = federate_db_obj.name
            events = selectors.EVENT_READ
            self.sel.register(ssock, events, federate)
            self.federates[server_vars[0]] = federate
            self._send_connected_clients(ssock)
            self.db.create_ActiveFederation(
                id=federate_db_obj.id,
                address=federate_db_obj.address,
                port=federate_db_obj.port,
                initiator="Self",
            )
            self.db.update_Federation(
                {"lastError": None}, query=f'id == "{federate_db_obj.id}"'
            )
            return None
        except Exception as e:
            try:
                self.db.remove_ActiveFederation(f'id == "{server_vars[0]}"')
            except Exception as e:
                self.logger.warning(
                    "exception thrown removing outgoing federation from DB " + str(e)
                )
            self.logger.warning("exception thrown creating new federation " + str(e))
            try:
                self.db.update_Federation(
                    {"status": "Disabled", "lastError": str(e)},
                    query=f'id == "{server_vars[0]}"',
                )
            except Exception as e:
                self.logger.warning(
                    "exception thrown updating federate in db " + str(e)
                )

    def receive_data_from_federate(self, timeout):
        """called whenever data is available from any federate and immediately proceeds to
        send data through process pipe
        """
        dataarray = []
        if self.federates:
            events = self.sel.select(timeout=timeout)
            for key, mask in events:
                conn = key.fileobj
                try:
                    header = conn.recv(4)
                except Exception as e:
                    continue
                if header:
                    try:
                        buffer = self._get_header_length(header)
                        raw_protobuf_message = conn.recv(buffer)
                        print(raw_protobuf_message)
                        protobuf_object = FederatedEvent()
                        protobuf_object.ParseFromString(raw_protobuf_message)
                        self.external_data_chain.Handle(self, protobuf_object)
                        dataarray.append(protobuf_object)
                    except Exception as e:
                        conn.recv(10000)
                        continue
                else:
                    self.disconnect_client(key.data.uid)
            return dataarray
        else:
            return None

    def start(self, pipe):
        self.db = DatabaseController()
        self.pipe = pipe
        self._create_context()
        print("started federation federate service")
        self.main()

    def stop(self):
        pass
