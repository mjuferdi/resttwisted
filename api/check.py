# -*- coding: utf-8 -*-

"""
Created on 27.09.2016

@author: juferdi
"""

from twisted.internet import defer
from restapi import RestAPI
import logging

_format = '%(asctime)s [%(levelname)s] -- %(message)s'
logging.basicConfig(format = _format, level=logging.DEBUG)
#filename='flexbb.log', 

class Check():
    """
    Basic Check class
    """
    def __init__(self):
        """
        Constructor.
        """
        self.api = RestAPI()
        self.logging = logging.getLogger('check.log')
        self.status = False
    
    def getAlive(self):
        """
        Called when result None or not OK.
        """
        return self.status
    
    def setAlive(self):
        """
        Called when result available.
        """
        self.status = True 
        
    @defer.inlineCallbacks
    def call(self, parId=None):
        """
        Check if server is reachable. Call setIsAlive and get from RestAPI.
        Parsing JSON response object in log file.
        @return: True if result available.
        @param parId: partitionId from object. 
        """
        self.logging.debug('>>Checking for Server status')
        try:
            if parId != None:
                self.api.setIsAliveId(parId)
            else:
                self.api.setIsAlive()
            json = yield self.api.get()
            if json is None:
                self.logging.warn('No response returned')
                self.getAlive()
            elif json['result'] != 'OK':
                self.logging.warn('Response: %s' % json['result'])
                self.getAlive()
            else:
                self.logging.info('Response: %s' % json['object'])
                self.setAlive()      
        except Exception as err:
            self.logging.error('Failed: %s' % err.message)
            defer.returnValue(False)
        defer.returnValue(True)
        
    @defer.inlineCallbacks
    def task(self, parId):
        """
        Check task for object.
        @param parId: partitionId from object. 
        """
        try:
            self.api.setTask(parId)
            json = yield self.api.get()
            if json is None:
                self.logging.warn('No response returned')
            elif json['result'] != 'OK':
                self.logging.warn('Response: %s' % json['result'])
                self.logging.info(json['object'])
            else:
                for item in json['object']:
                    id = int(item['elementId'])
                    type = int(item['elementType'])
                    state = item['elementState']
                    self.logging.info('Id: %d, Type: %d, State:%s' % (id, type, state))
        except Exception as err:
            self.logging.error('Failed: %s' % err.message)
            defer.returnValue(False)
        defer.returnValue(True)