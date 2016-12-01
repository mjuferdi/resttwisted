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
        Find object in database by parameter name.
        Call setSearch() or setSearchName() and get() from RestAPI.
        Parsing JSON response object in log file.
        @param name: object name to search 
        """
        try:
            if name != None:
                # Setup the URL with path ../search/name
                self.api.setSearchName(name)
                # Send http request with GET-method from api, and yield the result
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
                    self.setStatus()
            else:
                # Setup the URL path ../search
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
        except Exception as err:
            self.logging.error('Failed: %s' % err.message)
            defer.returnValue(err.message)
        defer.returnValue(json)
        
    @defer.inlineCallbacks
    def dirUpdate(self,name, stateUpdate):
        """
        Update status into database.
        Method search needs to be called first to get ID and Type.
        Call put() from RestAPI for updating status object.
        @param name: objects name. 
        @param stateUpdate: for new status to update.
        @return: resp is the result
        """
        try:
            # Get the object name from database server
            d = yield self.search(name)
            if d is False:
                defer.returnValue(False)
            if self.getStatus() == 0:
                self.logging.info('No name found for "%s"' % name)  
            self.api.setUpdate()
            if self.state == stateUpdate:
                self.logging.info('Not modified')
                defer.returnValue(d)
            else:
                # Create an object for update as body
                data= {'elementId': self.id,
                               'elementType': self.type,
                               'elementState': stateUpdate}
                # Send the http PUT request for update status object in database server by parameter object data
                resp = yield self.api.put(data)
                if resp['result'] == 'OK':
                    self.logging.info('Object have been modified')
                else:
                    self.logging.info(resp['result'])
                defer.returnValue(resp)
        except Exception as err:
            self.logging.error('Failed: %s' % err.message)
            defer.returnValue(None)
            
    @defer.inlineCallbacks
    def searchUpdate(self, objName, stateUpdate, partition=None):
        """
        Search name and direct update status.
        @param objName: object's name. 
        @param stateUpdate: for new status to update.
        @param partition: object's partition 
        @return: resp
        """
        try:
            # Setup the URL ../search
            self.api.setPutSearch()
            # Adjust the partition with the name of the object
            if 'DRES' in objName:
                partition = 'DRES'
            elif 'DVS' in objName:
                partition = 'DVS'
            elif 'AKW' in objName:
                partition = 'AKW'
            else:
                partition = None
            data = {'name': objName, 
                         'partition': partition, 
                         'state': stateUpdate}
             # Send the http PUT request for update status object in database server by parameter object data
            resp = yield self.api.put(data)
            if resp['result'] == 'OK':
                self.logging.info('%s is %s' % (objName, stateUpdate))
                defer.returnValue(resp)
            else:
                self.logging.warn('Response: %s' % resp['result'])
                self.logging.info('Object: %s' % resp['object'])
                defer.returnValue(resp)
        except Exception as err:
            self.logging.error('Failed: %s' % err.message)
            defer.returnValue(None)