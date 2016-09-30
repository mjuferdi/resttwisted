'''
Created on 27.09.2016

@author: juferdi
'''

from twisted.internet import defer, reactor
from twisted.internet.error import DNSLookupError
import unittest
from CheckConnection import Check
from twisted.web.client import Agent

test = Check()
class TestCase(unittest.TestCase):
        
    @defer.inlineCallbacks
    def testTrue(self):
        agent = Agent(reactor)
        d = yield agent.request('GET','http://localhost:8080/FlexBB/rest/isAlive', headers=None, bodyProducer=None )
        self.assertEqual(d.code, 200)
         
                                                                        
    @defer.inlineCallbacks
    def testFalse(self):
        try:
            agent = Agent(reactor)
            yield agent.request('GET','http://localhost:8080/FlexBB/rest/isAliverest', headers=None, bodyProducer=None )
        except DNSLookupError as e:
            print 'Error', e.message
        else:
            self.fail()
            
if __name__ == '__main__':
    unittest.main()