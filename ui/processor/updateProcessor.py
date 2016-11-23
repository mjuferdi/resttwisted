# -*- coding: utf-8 -*-

'''
Created on 22.11.2016

@author: juferdi
'''
from twisted.internet import defer
from twistedrest.ui.api import detector
import tkMessageBox

@defer.inlineCallbacks
def update(name, state):
    """
    Call for update state object in database
    @param name: objects name
    @param state: objects state
    @return: resp  
    """
    det = detector.Detector()
    json = yield det.dirUpdate(name, state)
    if json is None:
        tkMessageBox.showinfo('', 'Keine Updates mehr möglich')
        defer.returnValue(None)
    elif json['result'] == 'OK':
        elId = int(json['object']['elementId'])
        elSt = json['object']['elementState']
        elType = int(json['object']['elementType'])
        parId = int(json['object']['partitionId'])
        resp = 'Object: %s\nId: %d\nState: %s\nType: %d\nPartition id: %d' % (name, elId, elSt, elType, parId)
        defer.returnValue(resp)
    elif json['result'] == 'Not Modified':
        tkMessageBox.showinfo('', json['result'])
        defer.returnValue(None)