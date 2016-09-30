'''
Created on 26.09.2016

@author: juferdi
'''
from twisted.internet import defer
from RestAPI import RestAPI
import logging

_format = '%(asctime)s [%(levelname)s]-- %(message)s'
logging.basicConfig(format = _format, level = logging.DEBUG)
        
class FindDetector():
    """
        Base Class Detector.
        
        This class shows how to search detector, update status from dector and review
        detector status after updated. 
        Put argument as a name. 
    """
    def __init__(self,name):
        self.api = RestAPI()
        self.name = name
        self.id = 0
        self.type = 0
        self.state = ''
        self.status = {'isTrue':False}
        self.logging = logging.getLogger('search.log')
       
    def getStatus(self):
        """Return status"""
        return self.status['isTrue']
    
    def setStatus(self):
        """Set status"""
        self.status['isTrue'] = True
        
    @defer.inlineCallbacks
    def search(self): 
        """Find detector in Database"""
        
        try:
            self.logging.debug('>>Searching for "%s"' % self.name)
            self.api.setSearch(self.name)
            json = yield self.api.get()
            if json is None:
                self.logging.warn('No response returned')
                self.getStatus()
            elif json['result'] != 'OK':
                self.logging.warn('Response: %s' % json['result'])
                self.getStatus()
            else:
                self.id = int(json['object']['elementId'])
                self.type = int(json['object']['elementType'])  
                self.state = json['object']['elementState']
                self.logging.info('Found Detector: %s, Id: %s, Type: %s, State: %s' % (self.name, self.id, self.type, self.state))        
                self.setStatus()
                
        except Exception as err:
            self.logging.error('Failed: %s' % err.message)
      
    @defer.inlineCallbacks
    def update(self,state):
        """Update Data into database"""
        yield self.search()
        if self.getStatus() == 0:
            self.logging.info('No name found for "%s"' % self.name)  
        elif self.state == state:
            self.logging.debug('Not Modified')
        else:
            testdata= {'elementId': self.id,
                       'elementType': self.type,
                       'elementState': state}
            
            self.logging.debug('>>Update for "%s"' % self.name)
            self.logging.info('Update Id: %d, Type: %d, State: %s' % 
                           (testdata['elementId'], testdata['elementType'], testdata['elementState']))
            
            yield self.api.put(testdata)  
            
    @defer.inlineCallbacks
    def review(self):
        """To verify data updates that is already updated"""
        
        yield self.search()
        if self.getStatus() == 0:
            self.logging.info('No name found for "%s"' % self.name) 
        else:
            self.api.setStatus(self.id, self.type)
            json = yield self.api.get()
            self.logging.debug(json)
    