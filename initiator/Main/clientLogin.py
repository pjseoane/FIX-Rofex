"""FIX GATEWAY"""
import sys
import argparse
import configparser
import quickfix
from initiator.Main.fixEngine import fixEngine

def main(config_file):
#def main():
    """Main"""
    try:

        # *******Lectura de file de configuracion
        cpParser = configparser.RawConfigParser()
        cfgFile = r'../conf/usrCredentials.cfg'
        cpParser.read(cfgFile)
        usrId = cpParser.get('usr-credentials', 'usr')
        pswd = cpParser.get('usr-credentials', 'pswd')
        #************************

        settings = quickfix.SessionSettings(config_file)
        myFixApplication = fixEngine()
        myFixApplication.setUsrId(usrId)
        myFixApplication.setUsrPswd(pswd)

        storefactory = quickfix.FileStoreFactory(settings)
        logfactory = quickfix.FileLogFactory(settings)
        initiator = quickfix.SocketInitiator(myFixApplication, storefactory, settings, logfactory)

        initiator.start()
        myFixApplication.run()


        #while 1:
         #   myFixApplication.goRobot()

        initiator.stop()

    except (quickfix.ConfigError, quickfix.RuntimeError) as e:
        print(e)
        initiator.stop()
        sys.exit()


if __name__=='__main__':

    parser = argparse.ArgumentParser(description='FIX Client')
    parser.add_argument('file_name', type=str, help='Name of configuration file')
    args = parser.parse_args()

    main(args.file_name)


