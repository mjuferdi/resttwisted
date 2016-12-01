# -*- coding: utf-8 -*-

"""
Created on 26.09.2016

@author: juferdi

REST Client API

This is a REST webservice design for HTTP client side to send a request 
and get the response JSON object from Webserver. The Methods are GET and PUT available.
The REST is developed with Twisted framework.
"""

from twisted.internet import defer, reactor
from twisted.web.client import Agent, readBody
from twisted.web.iweb import IBodyProducer 
from twisted.web.http_headers import Headers
from twisted.internet.error import DNSLookupError
from logging import getLogger
from zope.interface import implements

import json
import tkMessageBox

class RestAPI():
    """
    Basic REST API class 
    
    Implementation http method GET and PUT for RestService, manage the URL path 
    and also produce a body for PUT method.
    """
    def __init__(self):
        """
        Constructors.
           
        Initialize an instance of Agent with a reactor for handling connection setup.
        """
        self.baseUrl = 'http://localhost:8080/FlexBB/rest/'
        self.agent = Agent(reactor)
        self.method = ''
        self.uri = ''
        self.encoder = json.encoder.JSONEncoder() 
        self.decoder = json.decoder.JSONDecoder()
        self.logging = getLogger('api.log')    
    
    def setIsAlive(self):
        """
        Called on call service.
        """
        self.uri = 'isAlive'
               
    def setIsAliveId(self, parId):
        """
        Called on call service.
        @param parId (int): partitionId.
        """
        self.uri = 'isAlive/' + '%d' % parId
        
    def setTask(self, parId):
        """
        Called on task service.
        @param parId (int): partitionId.
        """
        self.uri = 'task/' + '%d' % parId

    def setSearch(self):
        """
        Called on search service.
        """
        self.uri = 'search'
        
    def setSearchName(self, name):
        """
        Called on search service, 
        @param name (str): objects name.
        """
        self.uri = 'search/' + name
        
    def setStatus(self, _id, _typ):
        """
        Called on review service, 
        @param _id (int): elementId object
        @param _type (int): elementType object
        """
        self.uri = 'update/%d/%d' % (_id, _typ)
    
    def setUpdate(self):
        """
        Called on update service.
        """
        self.uri = 'update'
        
    def setPutSearch(self):
        """
        Called on update search service.
        """
        self.uri = 'search'
        
    @defer.inlineCallbacks    
    def get(self):
        """
        GET Method.
        
        Make an HTTP request with agent.request method. Minimum HTTP method and URL needed. 
        agent.request returns a Deferred that fires with a Response object.  
        defer.inlineCallbacks enabled generator return a Deferred object.
        If response code 200, result is available then yield it. Generator will automatically be resumed. 
        Or will fail with a failure object and raises an exception.
        defer.returnValue to return a value.
        @return: body content response.
        """
        try:
            d = yield self.agent.request('GET',
                                        self.baseUrl + self.uri, 
                                        headers=None,
                                        bodyProducer=None )
            
            self.logging.info('Status: {code} {phrase}'.format(code=d.code, phrase=d.phrase)) 
            if d.code == 200: 
                resp = yield readBody(d)           
                jData = self.decoder.decode(resp)   
                defer.returnValue(jData)
            else:
                defer.returnValue(None)  
        except DNSLookupError as err:
            self.logging.error('Error: %s' % err.message) 
            tkMessageBox.showwarning(' ', err.message)
            defer.returnValue(None)
    @defer.inlineCallbacks
    def put(self, obj):
        """
        PUT Method.
        Same as GET-Method. 
        In the PUT request, the object to be updated is supplied as an update object by the given URL.
        Header and bodyProducer is required as update object.  
        @return: response object.
        @param obj: Update-Object 
        """
        jBody = self.encoder.encode(obj)              
        header = Headers({'User-Agent': ['Python Twisted Rest'],
                          'Content-Type': ['application/json']})
        try:
            d = yield self.agent.request('PUT', 
                                         self.baseUrl + self.uri, 
                                         headers=header, 
                                         bodyProducer=StringProducer(jBody))
            self.logging.info('Status: {code} {phrase}'.format(code=d.code, phrase=d.phrase)) 
            if d.code == 200 or d.code == 204:
                resp = yield readBody(d)
                jData = self.decoder.decode(resp)
                defer.returnValue(jData)
            else:
                self.logging.info('Object have not been modified')
                defer.returnValue(None)              
        except DNSLookupError as err:
            self.logging.error('Error: %s' % err.message)
            defer.returnValue(None)
             
class StringProducer(object):
    """
    Produce the PUT data when the Agent needs it.
    """
    implements(IBodyProducer)

    def __init__(self, body):
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return defer.succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass