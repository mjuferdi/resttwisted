#-*- coding: utf-8 -*-

'''
Created on 22.11.2016

@author: juferdi
'''

from twisted.internet import defer
from api import restapi
import tkMessageBox

@defer.inlineCallbacks
def getPing():
    """
    Call for check if server is reachable.
    The respons object is shown in messagebox.
    
    """
    _api = restapi.RestAPI()
    try:
        # Setup URL with path ../isAlive
        _api.setIsAlive()
        # Send http GET request and return the result
        json = yield _api.get()
        if json is None:
            resp = 'Kein Respons-Objekt'
        elif json['result'] != 'OK':
            resp = json['result']
        else:
            resp = json['object']
        tkMessageBox.showinfo('', resp)
    except Exception as err:
        tkMessageBox.showerror('', err.message)