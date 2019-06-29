#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""

import sys
# from datetime import datetime
import quickfix as fix
import time
import logging
import threading

from initiator.model.logger import setup_logger
# from tornado import ioloop

__SOH__ = chr(1)

# Logger
setup_logger('FIX', 'Logs/message.log')
logfix = logging.getLogger('FIX')


class Application(fix.Application):
    """FIX Application"""

    def __init__(self):
         super().__init__()
         self.sessionID = None
         self.session_off = True
    #     self.io_loop = ioloop.IOLoop.current()


    def onCreate(self, sessionID):
        # onCreate is called when quickfix creates a new session.
        # A session comes into and remains in existence for the life of the application.
        # Sessions exist whether or not a counter party is connected to it.
        # As soon as a session is created, you can begin sending messages to it.
        # If no one is logged on, the messages will be sent at the time a connection is established with the counterparty.
        self.sessionID = sessionID
        # logger.info(f'onCreate sessionID: [{sessionID.toString()}], main: [{threading.main_thread().ident}], current[{threading.current_thread().ident}]')
        logfix.info("onCreate, sessionID >> (%s)" %self.sessionID)

    def onLogon(self, sessionID):
        # onLogon notifies you when a valid logon has been established with a counter party.
        # This is called when a connection has been established and the FIX logon process has completed with both parties exchanging valid logon messages.
        # logger.info(
        #     f'onLogon sessionID: [{sessionID.toString()}], main: [{threading.main_thread().ident}], current[{threading.current_thread().ident}]')
        logfix.info("onLogon, Hello Rofex: >> (%s)" % self.sessionID)
        self.session_off = False

    def onLogout(self, sessionID):
        # onLogout notifies you when an FIX session is no longer online.
        # This could happen during a normal logout exchange or because of a forced termination or a loss of network connection.
        # logger.info(
        #     f'onLogout sessionID: [{sessionID.toString()}], main: [{threading.main_thread().ident}], current[{threading.current_thread().ident}]')
        self.session_off = True
        logfix.info("onLogout, bye Rofex >> (%s)" % self.sessionID)


    def toAdmin(self, message, sessionID):
        # toAdmin provides you with a peek at the administrative messages that are being sent from your FIX engine
        # to the counter party. This is normally not useful for an application however it is provided for any logging
        # you may wish to do. Notice that the FIX::Message is not const.
        # This allows you to add fields to an adminstrative message before it is sent out.

        msg = message.toString().replace(__SOH__, "|")
        logfix.info("S toAdmin>> (%s)" % msg)

        if message.getHeader().getField(35) == "A":
            message.getHeader().setField(553, "pjseoane232")
            message.getHeader().setField(554, "AiZkiC5#")
            msg = message.toString().replace(__SOH__, "|")
            logfix.info("S toAdmin>> (%s)" % msg)
            # logger.info(f'toAdmin sessionID: [{sessionID.toString()}], message: [{message.toString()}], main: [{threading.main_thread().ident}], current[{threading.current_thread().ident}]')



    def fromAdmin(self, message, sessionID):
        # fromAdmin notifies you when an administrative message is sent from a counterparty to your FIX engine. This can be usefull for doing extra validation on logon messages like validating passwords.
        # Throwing a RejectLogon exception will disconnect the counterparty.
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("R adm>> (%s)" % msg)
        # logger.info(f'fromAdmin sessionID: [{sessionID.toString()}], message: [{message.toString()}], main: [{threading.main_thread().ident}], current[{threading.current_thread().ident}]')


    def toApp(self, message, sessionID):
        # toApp is a callback for application messages that are being sent to a counterparty.
        # If you throw a DoNotSend exception in this function, the application will not send the message.
        # This is mostly useful if the application has been asked to resend a message such as an order that is no longer relevant for the current market.
        # Messages that are being resent are marked with the PossDupFlag in the header set to true;
        # If a DoNotSend exception is thrown and the flag is set to true, a sequence reset will be sent in place of the message.
        # If it is set to false, the message will simply not be sent. Notice that the FIX::Message is not const.
        # This allows you to add fields to an application message before it is sent out.
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("S toApp>> (%s)" % msg)
        # logger.info(f'toApp sessionID: [{sessionID.toString()}], message: [{message.toString()}], main: [{threading.main_thread().ident}], current[{threading.current_thread().ident}]')
        self.getContractList()

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
        # msg = message.toString().replace(__SOH__, "|")
        # logfix.info("R app>> (%s)" % msg)

        self.onMessage(message, sessionID)
        # logger.info(f'fromApp sessionID: [{sessionID.toString()}], message: [{message.toString()}], main: [{threading.main_thread().ident}], current[{threading.current_thread().ident}]')


    def onMessage(self, message, sessionID):
        """on Message"""
        # Aca se procesan los mesajes que entran
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("onMessage, R app>> (%s)" % msg)

        pass

    def run(self):
        """Run"""
        while 1:
            time.sleep(2)
        # ioloop.IOLoop.current().start()


    def getContractList(self):


        msg=fix.Message()
        header=msg.getHeader()
         #
        header.setField(fix.BeginString(fix.BeginString_FIXT11))
        header.setField(fix.SenderCompID("pjseoane232"))
        header.setField(fix.TargetCompID("ROFX"))
        # header.setField(fix.MsgType(fix.MsgType_SecurityList))
        header.setField(fix.MsgType("y"))

        header.setField(fix.ApplVerID("7"))
         # header.setField(fix.SecurityReqID("d"))
         # header.setField(fix.SecurityListRequestType(4)) #fix.SecurityListRequestType_ALL_SECURITIES))

        fix.Session.sendToTarget(msg)
         # msg=fix.MsgType_SecurityList
         #
         # fix.Session.sendToTarget(msg) #,fix.SenderCompID("pjseoane232"),fix.TargetCompID("ROFX"))
        # message=fix.SecurityL
        # # header=message.
        # fix.SecurityReqID("c")
        # fix.SecurityListRequestType(0)
        # # message.SecurityListRequestType(559,"55")
        # # # message.setField(Text,("Lista de Contratos"))
        # fix.Session.sendToTarget(message,self.sessionID)

    def newOrder(self):

        # trade = fix.Message()
        # trade.getHeader().setField(fix.BeginString(fix.BeginString_FIX42))  #
        # trade.getHeader().setField(fix.MsgType(fix.MsgType_NewOrderSingle))  # 39=D
        # trade.setField(fix.ClOrdID(self.genExecID()))  # 11=Unique order
        #
        # trade.setField(fix.HandlInst(fix.HandlInst_MANUAL_ORDER_BEST_EXECUTION))  # 21=3 (Manual order, best executiona)
        # trade.setField(fix.Symbol('SMBL'))  # 55=SMBL ?
        # trade.setField(fix.Side(fix.Side_BUY))  # 43=1 Buy
        # trade.setField(fix.OrdType(fix.OrdType_LIMIT))  # 40=2 Limit order
        # trade.setField(fix.OrderQty(100))  # 38=100
        # trade.setField(fix.Price(10))
        # trade.setField(fix.TransactTime(int(datetime.utcnow().strftime("%s"))))
        # print
        # trade.toString()
        # fix.Session.sendToTarget(trade, self.sessionID)
        pass