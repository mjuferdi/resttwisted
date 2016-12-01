# -*- coding: utf-8 -*-

'''
Created on 22.11.2016

@author: juferdi
'''

from twisted.internet import defer
from api import restapi
import tkMessageBox

@defer.inlineCallbacks
def getInfo(name):
    """
    Call for get the objects information from database by parameter name.
    It's needed to call setSearchName() and get() from RestAPI class.
    @param name: objects name
    @return: resp 
    """
    _api = restapi.RestAPI()
    # If the return value more than one, it is added to a list myarr
    myarr = []
    if len(name) == 0:
        tkMessageBox.showinfo(' ', 'Bitte Objekt auswählen')
    try:
        for i in name:
            # Setup the URL with path ../search/name
            _api.setSearchName(i)
            # Send http GET request and return the respons object
            json = yield _api.get()
            # If there is not respons object, show this messagebox
            if json is None:
                tkMessageBox.showinfo('', 'Kein Respons-Objekt')
            else:
                elId = int(json['object']['elementId'])
                elSt = json['object']['elementState']
                elType = int(json['object']['elementType'])
                resp = 'Object: %s\nId: %d\nState: %s\nType: %d\n' % (i, elId, elSt, elType)
                myarr.append(resp)
        defer.returnValue(myarr)
    except Exception as err:
        tkMessageBox.showerror('', err.message)
        defer.returnValue(None)