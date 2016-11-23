'''
Created on 22.11.2016

@author: juferdi
'''
from twisted.internet import defer
from twistedrest.ui.api import restapi
import tkMessageBox

@defer.inlineCallbacks
def ping():
    """
    Check if server is reachable
    """
    _api = restapi.RestAPI()
    try:
        _api.setIsAlive()
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