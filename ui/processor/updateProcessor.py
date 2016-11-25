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
    myarr = []
    if len(name) == 0:
        tkMessageBox.showinfo(' ', 'Bitte Objekt auswählen')
    for i in name:
        json = yield det.dirUpdate(i, state)
        elId = int(json['object']['elementId'])
        elSt = json['object']['elementState']
        elType = int(json['object']['elementType'])
        parId = int(json['object']['partitionId'])
        resp = 'Object: %s\nId: %d\nState: %s\nType: %d\nPartition id: %d\n' % (i, elId, elSt, elType, parId)
        if json is None:
            myarr.append(resp)
        elif json['result'] == 'OK':
            myarr.append(resp)
        elif json['result'] == 'Not Modified':
            tkMessageBox.showinfo('', json['result'])
    defer.returnValue(myarr)