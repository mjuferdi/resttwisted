# -*- coding: utf-8 -*-

'''
Created on 22.11.2016

@author: juferdi
'''
from twisted.internet import defer
from twistedrest.ui.api import restapi
import tkMessageBox

@defer.inlineCallbacks
def task(parId):
    """
    Send http request task to server
    @param parId: Partition id from object
    @return: resp  
    """
    _api = restapi.RestAPI()
    try:
        respArr = []
        _api.setTask(parId)
        json = yield _api.get()
        if json is None:
            tkMessageBox.showinfo('', 'Kein Respons-Objekt')
            defer.returnValue(None)
        elif json['result'] == 'Not Found':
            resp = json['object']
            defer.returnValue(resp)
        elif json['result'] == 'OK':
            for item in json['object']:
                elId = int(item['elementId'])
                elType = int(item['elementType'])
                elSt = item['elementState']
                resp = 'Id: %d\nType: %s\nPartition id: %d\nState: %s' % (elId, elType, parId, elSt)
                respArr.append(resp)
            defer.returnValue(respArr)
    except Exception as err:
        tkMessageBox.showerror('', err.message)
        defer.returnValue(None)