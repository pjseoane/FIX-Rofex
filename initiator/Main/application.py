#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""

import sys
# from datetime import datetime
import quickfix as fix
import time
import logging

from initiator.model.logger import setup_logger
from initiator.model import Field


# configured
__SOH__ = chr(1)

# Logger
setup_logger('FIX', 'Logs/message.log')
logfix = logging.getLogger('FIX')


class Application(fix.Application):
    """FIX Application"""

    def onCreate(self, sessionID):
        # onCreate is called when quickfix creates a new session.
        # A session comes into and remains in existence for the life of the application.
        # Sessions exist whether or not a counter party is connected to it.
        # As soon as a session is created, you can begin sending messages to it.
        # If no one is logged on, the messages will be sent at the time a connection is established with the counterparty.
        self.sessionID = sessionID
        print("On Create")
        return

    def onLogon(self, sessionID):
        # onLogon notifies you when a valid logon has been established with a counter party.
        # This is called when a connection has been established and the FIX logon process has completed with both parties exchanging valid logon messages.
        self.sessionID = sessionID
        print("I'm in !.. hello Rofex")
        return

    def onLogout(self, sessionID):
        # onLogout notifies you when an FIX session is no longer online.
        # This could happen during a normal logout exchange or because of a forced termination or a loss of network connection.
        print("...on Logout")
        return

    def toAdmin(self, message, sessionID):
        # toAdmin provides you with a peek at the administrative messages that are being sent from your FIX engine
        # to the counter party. This is normally not useful for an application however it is provided for any logging
        # you may wish to do. Notice that the FIX::Message is not const.
        # This allows you to add fields to an adminstrative message before it is sent out.

        msg = message.toString().replace(__SOH__, "|")
        logfix.info("S >> (%s)" % msg)

        if message.getHeader().getField(35) == "A":
            message.getHeader().setField(553, "pjseoane232")
            message.getHeader().setField(554, "AiZkiC5#")
            print("Message 35")

        print("Mensaje toAdmin")
        return

    def fromAdmin(self, message, sessionID):
        # fromAdmin notifies you when an administrative message is sent from a counterparty to your FIX engine. This can be usefull for doing extra validation on logon messages like validating passwords.
        # Throwing a RejectLogon exception will disconnect the counterparty.
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("R >> (%s)" % msg)
        return

    def toApp(self, message, sessionID):
        # toApp is a callback for application messages that are being sent to a counterparty.
        # If you throw a DoNotSend exception in this function, the application will not send the message.
        # This is mostly useful if the application has been asked to resend a message such as an order that is no longer relevant for the current market.
        # Messages that are being resent are marked with the PossDupFlag in the header set to true;
        # If a DoNotSend exception is thrown and the flag is set to true, a sequence reset will be sent in place of the message.
        # If it is set to false, the message will simply not be sent. Notice that the FIX::Message is not const.
        # This allows you to add fields to an application message before it is sent out.
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("S >> (%s)" % msg)
        return

    def fromApp(self, message, sessionID):
        # fromApp receives application level request.
        # If your application is a sell-side OMS, this is where you will get your new order requests.
        # If you were a buy side, you would get your execution reports here.
        # If a FieldNotFound exception is thrown,
        # the counterparty will receive a reject indicating a conditionally required field is missing.
        # The Message class will throw this exception when trying to retrieve a missing field, so you will rarely need the throw this explicitly.
        # You can also throw an UnsupportedMessageType exception.
        # This will result in the counterparty getting a reject informing them your application cannot process those types of messages.
        # An IncorrectTagValue can also be thrown if a field contains a value you do not support.
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("R >> (%s)" % msg)
        self.onMessage(message, sessionID)
        return

   
    def onMessage(self, message, sessionID):
        """on Message"""
        print("On Message")
        pass

    def run(self):
        """Run"""
        while 1:
            time.sleep(2)