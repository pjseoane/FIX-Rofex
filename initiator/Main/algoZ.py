from initiator.Main import clientLogin as cl



class cAlgoZ(cl.clientLogin):

    def __init__(self):
        super().__init__()

    def goRobot(self):
        # def securityListRequest(self):
        # pag 73

        msg = cl.buildMsgHeader("x")

        msg.setField(cl.SecurityReqID(self.ListaContratos))
        msg.setField(cl.SecurityListRequestType(0))
        # msg.setField(fe.MarketID("ROFX"))
        # msg.setField(fe.MarketSegmentID('DDF'))

        msg.setField(cl.Symbol("RFX20Jun20"))
        msg.setField(cl.SecurityExchange('ROFX'))
        msg.setField(cl.CFICode("FXXXSX"))

        cl.Session.sendToTarget(msg)
        # #---------------------------------------------------------

if __name__ == '__main__':
    aZero= cAlgoZ()