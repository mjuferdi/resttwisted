'''
Created on 26.09.2016

@author: juferdi
'''

from twisted.internet import defer, reactor
from twisted.web.client import Agent, readBody
from twisted.web.iweb import IBodyProducer 
from twisted.web.http_headers import Headers
from twisted.internet.error import DNSLookupError
from logging import getLogger
from zope.interface import implements

import json

class RestAPI():
    """REST API"""
    
    def __init__(self):
        self.baseUrl = 'http://localhost:8080/FlexBB/rest/'
        self.agent = Agent(reactor)
        self.method = ''
        self.uri = ''
        self.encoder = json.encoder.JSONEncoder()
        self.decoder = json.decoder.JSONDecoder()
        self.logging = getLogger('api.log')    
        
    def setIsAlive(self):
        self.uri = 'isAlive/'

    def setSearch(self, name):
        self.uri = 'search/' + name
        
    def setStatus(self, _id, _typ):
        self.uri = 'update/%d/%d' % (_id, _typ)
        
    @defer.inlineCallbacks    
    def get(self):
        """GET Method
            
           Return body response. 
        """
        try:
            d = yield self.agent.request('GET',
                                        self.baseUrl + self.uri, 
                                        headers=None,
                                        bodyProducer=None )
            
            self.logging.info('Status: %s %s' % (d.code, d.phrase)) 
            
            if d.code == 200: 
                resp = yield readBody(d)
                jData = self.decoder.decode(resp)
                defer.returnValue(jData)
            else:
                defer.returnValue(None)  
        except DNSLookupError as err:
            self.logging.error('Error: %s' % err.message) 
            defer.returnValue(None)

    @defer.inlineCallbacks
    def put(self, obj):
        """PUT Method
            
           Return body response.
        """
        uri = '%s%s' % (self.baseUrl,'update/')
        jBody = self.encoder.encode(obj)    
                       
        header = Headers({'User-Agent': ['Python Twisted Rest'],
                          'Content-Type': ['application/json']})
        try:
            d = yield self.agent.request('PUT', 
                                         uri, 
                                         headers=header, 
                                         bodyProducer=StringProducer(jBody))
            
            self.logging.info('Status: %s %s' % (d.code, d.phrase)) 
            if d.code == 200 or d.code == 204:
                resp = yield readBody(d)
                jData = self.decoder.decode(resp) 
                self.logging.info('Object have been modified')
                defer.returnValue(jData)
            else:
                self.logging.warn('Object have not been modified')
                defer.returnValue(None)              
        except DNSLookupError as err:
            self.logging.error('Error: %s' % err.message)
            defer.returnValue(None)
        
class StringProducer(object):
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
