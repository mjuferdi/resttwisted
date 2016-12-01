# -*- coding: utf-8 -*-

'''
Created on 22.11.2016

@author: juferdi
'''

from twisted.internet import defer
from api import restapi
import tkMessageBox

@defer.inlineCallbacks
def getTask(parId):
    """
    Send http GET request task by partition id to server and return the respons object.
    @param parId: Partition id from object
    @return: resp  
    """
    _api = restapi.RestAPI()
    # If the return value more than one, it is added to a list myarr
    respArr = []
    try:
        # Setup the URL with path ../task/partitionId
        _api.setTask(parId)
        json = yield _api.get()
        if json is None:
            tkMessageBox.showinfo('', 'Kein Respons-Objekt')
            defer.returnValue(None)
        elif json['result'] == 'Not Found':
            tkMessageBox.showinfo('', json['object'])
            defer.returnValue(None)
        elif json['result'] == 'OK':
            for item in json['object']:
                elId = int(item['elementId'])
                elType = int(item['elementType'])
                elSt = item['elementState']
                resp = 'Id: %d\nType: %s\nPartition id: %d\nState: %s\n' % (elId, elType, parId, elSt)
                respArr.append(resp)
            defer.returnValue(respArr)
    except Exception as err:
        tkMessageBox.showerror('', err.message)
        defer.returnValue(None)