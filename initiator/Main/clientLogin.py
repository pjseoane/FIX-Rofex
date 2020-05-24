"""FIX GATEWAY"""
import sys
import argparse
import configparser
import quickfix as fix
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

        settings = fix.SessionSettings(config_file)
        myFixApplication = fixEngine()
        myFixApplication.setUsrId(usrId)
        myFixApplication.setUsrPswd(pswd)

        storefactory = fix.FileStoreFactory(settings)
        logfactory = fix.FileLogFactory(settings)
        initiator = fix.SocketInitiator(myFixApplication, storefactory, settings, logfactory)

        initiator.start()
        myFixApplication.run()
        initiator.stop()

    except (fix.ConfigError, fix.RuntimeError) as e:
        print(e)
        initiator.stop()
        sys.exit()


if __name__=='__main__':

    parser = argparse.ArgumentParser(description='FIX Client')
    parser.add_argument('file_name', type=str, help='Name of configuration file')
    args = parser.parse_args()

    main(args.file_name)


