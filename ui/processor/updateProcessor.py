# -*- coding: utf-8 -*-

'''
Created on 22.11.2016

@author: juferdi
'''

from twisted.internet import defer
from api import detector
import tkMessageBox


@defer.inlineCallbacks
def getUpdate(name, state):
    """
    Call for update state object in database, than return the respons object.
    To do that, it needs to call a function dirUpdate() from Detector class.
    @param name: objects name
    @param state: objects state
    @return: myarr  
    """
    det = detector.Detector()
    # If return value more than one, it is added to a list myarr
    myarr = []
    if len(name) == 0:
        tkMessageBox.showinfo(' ', 'Bitte Objekt auswählen')
    for i in name:
        json = yield det.dirUpdate(i, state)
        elId = int(json['object']['elementId'])
        elSt = json['object']['elementState']
        elType = int(json['object']['elementType'])
        resp = 'Object: %s\nId: %d\nState: %s\nType: %d\n' % (i, elId, elSt, elType)
        if json is None:
            myarr.append(resp)
        elif json['result'] == 'OK':
            myarr.append(resp)
        elif json['result'] == 'Not Modified':
            tkMessageBox.showinfo('', json['result'])
    defer.returnValue(myarr)