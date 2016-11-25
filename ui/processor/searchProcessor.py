# -*- coding: utf-8 -*-

'''
Created on 22.11.2016

@author: juferdi
'''
from twisted.internet import defer
from twistedrest.ui.api import restapi
import tkMessageBox
@defer.inlineCallbacks
def getList():
    """
    Get all list's objects from database
    @return: resp
    """
    _api = restapi.RestAPI()
    resp = []
    _api.setSearch()
    json = yield _api.get()
    if json is None:
        tkMessageBox.showwarning('', 'Keine Liste vorhanden')
        defer.returnValue(None)
    else:
        for item in json['object']:
            resp.append(item)
        defer.returnValue(resp)