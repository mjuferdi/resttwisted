'''
Created on 27.09.2016

@author: juferdi
'''
from twisted.internet import defer
from RestAPI import RestAPI
import logging

_format = '%(asctime)s [%(levelname)s] -- %(message)s'
logging.basicConfig(format = _format, level=logging.DEBUG)

class Check():
    """
        Base Check class.
        
        To check the connection with server.
    """
    
    def __init__(self):
        self.api = RestAPI()
        self.logging = logging.getLogger('check.log')
        self.status = False
        self.logging.debug('>>Checking for Server status')
    
    def getAlive(self):
        "Return status"
        return self.status
    
    def setAlive(self):
        "Set status True"
        self.status = True 
        
    @defer.inlineCallbacks
    def call(self):
        """Call server and waiting for response from the server"""
        
        try:
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
            
        self.logging.info('Check done.')
        defer.returnValue(True)
            