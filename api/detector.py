# -*- coding: utf-8 -*-

"""
Created on 26.09.2016

@author: juferdi
"""
from twisted.internet import defer
from restapi import RestAPI
import logging

_format = '%(asctime)s [%(levelname)s]-- %(message)s'
logging.basicConfig(format = _format, level = logging.DEBUG)
        
class Detector():
    """
    Basic Detector class
    """
    def __init__(self):
        """
        Constructor.
        
        Initialize global RestAPI object.
        """
        self.api = RestAPI()
        self.id = 0
        self.type = 0
        self.parId = 0
        self.zone = 0
        self.name = ''
        self.state = ''
        self.status = {'isTrue':False}
        self.logging = logging.getLogger('search.log')
       
    def getStatus(self):
        """
        Called when result None or not OK.
        """
        return self.status['isTrue']
    
    def setStatus(self):
        """
        Called when result available.
        """
        self.status['isTrue'] = True
        
    @defer.inlineCallbacks
    def search(self, name = None): 
        """
        Find object in database.
            
        Call setSearch and get from RestAPI.
        Parsing JSON response object in log file.
        @param name: object name to search 
        """
        self.logging.debug('>>Searching for "%s"' % name)
        try:
            if name != None:
                self.api.setSearchName(name)
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
                    self.parId = int(json['object']['partitionId']) 
                    self.logging.info('Name: %s, Id: %d, Type: %d, PartitionId: %d, State: %s' % (name, self.id, self.type, self.parId, self.state))        
                    self.setStatus()
            else:
                self.api.setSearch()   
                json = yield self.api.get()
                if json is None:
                    self.logging.warn('No response returned')
                    self.getStatus()
                else:
                    self.logging.info(json['result'])
                    for item in json['object']:
                        self.name = item['name']
                        self.id = int(item['id'])
                        self.type = int(item['elementtype']) 
                        self.zone = int(item['flexzoneid']) 
                        self.logging.info('Name: %s, Id:%d, Type:%d, Zone:%d' % (self.name, self.id, self.type, self.zone))  
        except Exception as err:
            self.logging.error('Failed: %s' % err.message)
            defer.returnValue(False)
        defer.returnValue(True)
         
    @defer.inlineCallbacks
    def dirUpdate(self,name, stateUpdate):
        """
        Update status into database.
        
        Method search needs to be called first to get ID and Type.
        Call put from RestAPI for updating status object.
        @param name: objects name. 
        @param stateUpdate: for new status to update.
        @param data: an update object.
        """
        try:
            d = yield self.search(name)
            if d is False:
                defer.returnValue(False)
            if self.getStatus() == 0:
                self.logging.info('No name found for "%s"' % name)  
            self.api.setUpdate()
            if self.state == stateUpdate:
                self.logging.info('Not modified')
            else:
                data= {'elementId': self.id,
                               'elementType': self.type,
                               'elementState': stateUpdate}
                    
                self.logging.debug('>>Update for %s' % name)
                self.logging.info('Updated State: %s' % data['elementState'])
                resp = yield self.api.put(data)
                if resp['result'] == 'OK':
                    self.logging.info('Object have been modified')
                else:
                    self.logging.info(resp['result'])
        except Exception as err:
            self.logging.error('Failed: %s' % err.message)
            defer.returnValue(False)
        defer.returnValue(True)
        
    @defer.inlineCallbacks
    def searchUpdate(self, objName, stateUpdate):
        """
        Search name and direct update status.
        @param name: objects name. 
        @param stateUpdate: for new status to update.
        """
        try:
            self.api.setPutSearch()
            data = {'name': objName, 
                         'partition': None, 
                         'state': stateUpdate}
            self.logging.info('Searching for %s and updating status: %s' % (objName, data['state']))
            resp = yield self.api.put(data)
            if resp['result'] == 'OK':
                self.logging.info('%s is %s' % (objName, stateUpdate))
            else:
                self.logging.warn('Response: %s' % resp['result'])
                self.logging.info('Object: %s' % resp['object'])
        except Exception as err:
            self.logging.error('Failed: %s' % err.message)
            defer.returnValue(False)
        defer.returnValue(True)
            
    @defer.inlineCallbacks
    def review(self, name):
        """
        To verify data update that is already updated.
        @param name: objects name.
        """
        d = yield self.search(name)
        if d is False:
            defer.returnValue(False)
        if self.getStatus() == 0:
            self.logging.info('No name found for "%s"' % name) 
        else:
            self.api.setStatus(self.id, self.type)
            json = yield self.api.get()
            self.logging.info(json)
        defer.returnValue(True)