# -*- coding: utf-8 -*-

"""
Created on 20.10.2016

@author: juferdi
"""

from check import Check
from detector import Detector
from config import Config
from twisted.internet import reactor, defer
import sys
import time

class Processor():
    """
    Basic Processor class
    """
    def __init__(self):
        self.ch = Check()
        self.de = Detector()
        self.con = Config()
        self.opt = ''
        self.arg = ''
        self.state = ''
        self.parId = None
        self.name = None
        self.resp = None
        self.num = 1
        self.done = 0
        self.delay = 0
        self.th = 0
        self.q = []
        self.plot = False
        self.ret = {'isThread':False}
        self.cmd = {'onlyOpt' : True}
        
    def setPlot(self):
        """
        Called when argument Chart is given.
        """
        self.plot = True
      
    def isThread(self):
        """
        Called when argument Thread is given.
        """
        self.ret['isThread'] = True
        
    def setCommand(self):
        """
        Called once to check if command exist
        """
        self.cmd['onlyOpt'] = False
        
    def stopWorker(self, ignored):
        """
        Once the connection has been terminated, stop the reactor. 
        And show the diagram, when argument is given.
        @return: ignored
        """
        if self.ret['isThread'] is True:
            self.done += 1
            if self.done == self.th:
                if self.plot is True:
                    self.con.setPlot(self.q, isThread = True)
                reactor.stop() 
        else:
            if self.plot is True:
                self.con.setPlot(self.q, isThread = False)
            reactor.stop()
               
    def doWorker(self):
        """
        Register a callback.
        """
        d = self.worker()
        d.addCallback(self.stopWorker)  

    def getMethod(self): 
        """
        Manage user argument as parameter for GET-method.
        """
        if self.arg[0] in ('ping', 'search') and len(self.arg) == 1:
            self.parId = None
        elif self.arg[0] in ('ping', 'task'):
            if len(self.arg) > 1 and len(self.arg) == 2: 
                self.parId = int(self.arg[1]) 
                if self.parId < 0: raise Exception
            else: raise Exception
        elif self.arg[0] in ('search', 'status'):
            if len(self.arg) > 1 and len(self.arg) == 2:
                self.name = self.arg[1]
            else: raise Exception
        else:
            raise Exception
        self.setCommand()
        
    def putMethod(self):
        """
        Manage user argument as parameter for PUT-method.
        """
        if len(self.arg) > 1 and len(self.arg) == 2:
            self.name = self.arg[0]
            self.state = self.arg[1]
        elif self.arg[0] == 'search' and len(self.arg) > 1 and len(self.arg) == 3:
            self.name = self.arg[1]
            self.state = self.arg[2]
        else:
            raise Exception
        self.setCommand()
        
    def setup(self):
        """
        Called to set up, if there are multiple request running simultaneously.
        """
        if self.cmd['onlyOpt'] is False:
            if self.ret['isThread'] is True:
                for m in xrange(self.th):
                    self.doWorker()
            else:
                self.doWorker()
        else:
            raise Exception
            
    @defer.inlineCallbacks
    def worker(self):
        """
        Using RESTApi to execute commands with the given parameters and 
        adding a time value to the list.
        Print text for the result.
        @return: var resp as response object.
        """
        oke = 0
        notoke = 0
        latecyList = [0,]
        timeList = [0,]
        tookList = []
        try:
            start = time.time()
            for n in xrange(self.num):
                s = time.time()
                if self.opt in ('-g', '--get'):
                    if self.arg[0] == 'ping':
                        resp = yield self.ch.call(self.parId)
                    elif self.arg[0] == 'task':
                        resp = yield self.ch.task(self.parId)
                    elif self.arg[0] == 'search':
                        resp = yield self.de.search(self.name)
                    elif self.arg[0] == 'status':
                        resp = yield self.de.review(self.name)
                elif self.opt in ('-p','--put'):
                    if self.arg[0] == 'search':
                        resp = yield self.de.searchUpdate(self.name, self.state)
                    else:
                        resp = yield self.de.dirUpdate(self.name, self.state)
                else: raise Exception
                e = time.time()
                if resp is True:
                    oke += 1
                else:
                    notoke += 1
                time.sleep(self.delay)
                st = round((e-start),2)
                r = int(round((e-s)*1000))
                latecyList.append(r)
                timeList.append(st)
            end = time.time()
            res = int(round((end-start)*1000))
            avg = int(round(res/self.num))
            tookList.append(end-start)
            self.q.append((latecyList[:], timeList[:], tookList[:]))
        except Exception as err:
            print err.message
        finally:
            text = """Finished......
Generated:   %s
Complete requests:   %s 
Failed requests:     %s
Total taken:         %s [ms] (mean)
Time per request:    %s [ms] (mean, across all concurrent requests) 
    Connection Times (ms)
     min:    %s 
     max:    %s\n""" % (self.num, oke, notoke, res, avg, min(latecyList[1:]), max(latecyList))
            print text 
