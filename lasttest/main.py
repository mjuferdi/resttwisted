#!/usr/bin/python
# -*- coding: utf-8 -*-

from processor import Processor
from config import Config
from twisted.internet import reactor
import sys
import getopt

def main():
    """
    Access command line arguments and options.
    Run the reactor, which will kick off the HTTP request.
    """
    pro = Processor()
    con = Config()
    i = None
    try:
        if len(sys.argv) == 1: raise Exception
        opts, args = getopt.getopt(sys.argv[1:], "hg:p:n:T:d:c:", ["help","get=","put="])
        for opt, arg in opts:
            if opt in ('-h', '--help'): 
                con.help()
            elif opt in ('-g', '--get'):
                if len(arg) > 1:
                    i = arg.split(',')
                pro.arg = i
                pro.getMethod()
            elif opt in ('-p', '--put'):
                i = arg
                if len(i) > 1:
                    i = arg.split(',')
                else:
                    raise Exception
                pro.arg = i
                pro.putMethod()
            elif opt in ('-n'):
                pro.num = int(arg)
                if pro.num <=0: raise Exception
            elif opt in ('-T'):
                pro.th = int(arg)
                if pro.th <=0 or pro.th >=8:
                    print 'Number of Threads not allowed (max 7).'
                    raise Exception
                pro.isThread()
            elif opt in ('-d'):
                pro.delay = float(arg)
                if pro.delay < 0: raise Exception
            elif opt in  ('-c'):
                if arg == 'on':
                    pro.plot = True
                else: raise Exception
            else:
                raise Exception
        pro.setup()
    except Exception:
        con.errorHandling()
              
if __name__ == '__main__':
    main()
    reactor.run()