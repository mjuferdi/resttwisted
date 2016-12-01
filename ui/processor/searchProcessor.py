# -*- coding: utf-8 -*-

'''
Created on 22.11.2016

@author: juferdi
'''

from twisted.internet import defer
from api import restapi
from api import detector
import tkMessageBox

@defer.inlineCallbacks
def getList():
    """
    Get all list's objects from database. All objects are added to a list and returned.
    @return: resp
    """
    _api = restapi.RestAPI()
    resp = []
    # Setup URL with path ../search
    _api.setSearch()
    json = yield _api.get()
    if json is None:
        tkMessageBox.showwarning('', 'Keine Liste vorhanden')
        defer.returnValue(None)
    else:
        for item in json['object']:
            resp.append(item)
        defer.returnValue(resp)
        
@defer.inlineCallbacks
def getSearchUpdate(objName, stateUpdate, partition=None):
    """
    Using a function searchUpdate() with some parameters from Detector's Class to
    organize respons object and return the value resp.
    @param objName: object's name
    @param stateUpdate: new status for update
    @param partition: object's partition
    @return: resp
    """
    det = detector.Detector()
    json = yield det.searchUpdate(objName, stateUpdate, partition)
    if json is None:
        tkMessageBox.showinfo(' ', 'Kein Update möglich')
        defer.returnValue(None)
    elif json['result'] == 'OK':
        elId = int(json['object']['elementId'])
        elType = int(json['object']['elementType'])
        parId = int(json['object']['partitionId'])
        elSt = json['object']['elementState']
        resp = 'Object: %s\nId: %d\nType: %d\nPartition id: %d\nState: %s' % (objName, elId, elType, parId, elSt)
        defer.returnValue(resp)
    else:
        resp = json['object']
        tkMessageBox.showinfo(' ', 'Objekt nicht gefunden')
        defer.returnValue(resp)
            
        
        
