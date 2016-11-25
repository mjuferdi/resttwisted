# -*- coding: utf-8 -*-

'''
Created on 22.11.2016

@author: juferdi
'''
from twisted.internet import defer
from twistedrest.ui.api import restapi
import tkMessageBox

@defer.inlineCallbacks
def getInfo(name):
    """
    Call for object in database and get the objects information
    @param name: objects name
    @return: resp 
    """
    _api = restapi.RestAPI()
    myarr = []
    if len(name) == 0:
        tkMessageBox.showinfo(' ', 'Bitte Objekt auswählen')
    try:
        for i in name:
            _api.setSearchName(i)
            json = yield _api.get()
            if json is None:
                tkMessageBox.showinfo('', 'Kein Respons-Objekt')
            else:
                elId = int(json['object']['elementId'])
                elSt = json['object']['elementState']
                elType = int(json['object']['elementType'])
                parId = int(json['object']['partitionId'])
                resp = 'Object: %s\nId: %d\nState: %s\nType: %d\nPartition id: %d\n' % (i, elId, elSt, elType, parId)
                myarr.append(resp)
        defer.returnValue(myarr)
    except Exception as err:
        tkMessageBox.showerror('', err.message)
        defer.returnValue(None)