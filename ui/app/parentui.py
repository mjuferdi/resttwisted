#-*- coding: utf-8 -*-

'''
Created on 16.11.2016

@author: juferdi
'''
from twistedrest.ui.processor import pingProcessor
from twistedrest.ui.processor import searchProcessor
from twistedrest.ui.processor import getInfoProcessor
from twistedrest.ui.processor import updateProcessor

from childui import SubApp
from Tkinter import *
from twisted.internet import reactor, tksupport
from ScrolledText import ScrolledText
from ttk import Combobox
import tkMessageBox

class App(object):
    """Basic Class App"""
    def __init__(self, master):
        """
        Konstruktor
        Setup widgets
        """
        self.resp = []
        self.listname = []
        self.state = {'State':''}
        master.title('FlexBB')
        master.rowconfigure(0, weight=1)
        master.columnconfigure(0, weight=1)
        master.resizable(False, False)
        
        #create labelframe1
        lfLeft = LabelFrame(master, text='Melder-Liste')
        lfLeft.grid(row=0, column=0, columnspan=4, sticky=W+N+S,
                    padx=5, pady=5, ipadx=5, ipady=5)
        
        #create label search
        lbSearch = Label(lfLeft, text='Geben Sie Melder-Name ein :')
        lbSearch.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        
        #create combobox
        opt = ('Sortiere nach:', 'Flexzone', 'Element type')
        self.cbSort = Combobox(lfLeft, values=opt, state='readonly')
        self.cbSort.current(0)
        self.cbSort.bind('<<ComboboxSelected>>', self.displayListObj)
        self.cbSort.grid(row=3, padx=5, sticky=W)
        self.cbSort.config(state=DISABLED)
        
        #create entrybox
        self.eSearch = Entry(lfLeft)
        self.eSearch.grid(row=0, column=1, padx=5, pady=2)
        self.eSearch.config(state=DISABLED)
        
        #create button search
        self.btSearch = Button(lfLeft, text='Get Liste', command=self.getList)
        self.btSearch.grid(row=0, column=2, padx=5, pady=2)
        
        #create scrollbar
        sb = Scrollbar(lfLeft)
        sb.grid(row=4, column=3, pady=5, sticky=N+S)
        
        #create listbox
        self.lbList = Listbox(lfLeft, yscrollcommand=sb.set, height=20)
        self.lbList.grid(row=4, columnspan=3, padx=5, pady=5, sticky=W+E)
        sb.config(command=self.lbList.yview)
        
        #create labelframe2
        self.lfRight = LabelFrame(master, text='Information')
        self.lfRight.grid(row=0, column=6, sticky=N+S, padx=5, pady=5, ipadx=5, ipady=5)
        
        #create scrolltext info
        self.stInfo = ScrolledText(self.lfRight, width=35, height=10)
        self.stInfo.grid(row=0, columnspan=3, padx=5, sticky=W+E)
        
        #create check server
        btIsAlive = Button(self.lfRight, text='Check Server', command=pingProcessor.ping)
        btIsAlive.grid(row=5, columnspan=1, padx=5, pady=5, sticky=W+E)
        
        #create button GET
        self.btGet = Button(self.lfRight, text='GET', command=self.getInfoObj)
        self.btGet.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky=W+E)
        self.btGet.config(state=DISABLED)
        
        #create button on
        btOn = Button(self.lfRight, text='ON', command=self.setStateOn)
        btOn.grid(row=2, columnspan=3, padx=5, pady=5, sticky=W+E)
        
        #create button off
        btOff = Button(self.lfRight, text='OFF', command=self.setStateOff)
        btOff.grid(row=3, columnspan=3, padx=5, pady=5, sticky=W+E)
        
        #create button check
        btCheck = Button(self.lfRight, text='CHECK', command=self.setStateCheck)
        btCheck.grid(row=4, columnspan=3, padx=5, pady=5, sticky=W+E)
        
        #create button task
        btTask = Button(self.lfRight, text='Task', command=self.openSubApp)
        btTask.grid(row=5, column=1, columnspan=2, padx=5, pady=5, sticky=W+E)
        
        #create button on
        btExit = Button(self.lfRight, text='Exit', command=self.exit)
        btExit.grid(row=6, padx=5, pady=5, sticky=W)
        
    def getList(self):
        """
        Show all object or search given object's name and put in listbox
        Register a callback to function callback
        """
        self.btSearch['text'] = 'Suche'
        self.eSearch.config(state=NORMAL)
        self.btGet.config(state=NORMAL)
        self.cbSort.config(state=NORMAL)
        self.lbList.delete(0, END)
        _input = self.eSearch.get()
        if not _input:
            d = searchProcessor.getList()
            d.addCallback(self.callback)
        elif _input in self.listname:
            self.lbList.insert(END,_input)
        elif _input not in self.listname:
            tkMessageBox.showinfo('', 'No name for "%s"' % _input)
             
    def callback(self, resp):
        """
        Set global variable resp
        Create new list contains only name
        @param resp: respons-object 
        """
        self.resp = resp
        self.listname = map(lambda d: d['name'], self.resp)
        self.displayListObj(self.resp)
        
    def displayListObj(self, resp):
        """
        Display response object in listbox
        @param resp: response object 
        """
        try:
            resp = self.resp
            value = self.cbSort.get()
            self.stInfo.config(state=NORMAL)             
            self.stInfo.delete(1.0, END)
            self.lbList.delete(0,END)
            if value == 'Sortiere nach:':
                for item in resp:
                    self.lbList.insert(END, item['name'])
            elif value == 'Flexzone':
                self.sortList(0, 'flexzoneid', 9, 'Flexzone id ')
            elif value == 'Element type':
                self.sortList(1, 'elementtype', 3, 'Element type ')
        except:
            return None
    
    def sortList(self, num, key, ran, text):
        """
        Option sort list
        @param num: int parameter
        @param key: key in list of dict
        @param ran: range for do looping
        @param text: output text   
        """
        i = num
        newlist = sorted(self.resp, key=lambda k: k[key])
        for x in range(ran):
            myarr = []
            self.lbList.insert(END, text + '%d :' % i)
            for item in newlist: 
                if item[key] == i:
                    myarr.append(item['name'])
            for d in myarr:
                self.lbList.insert(END, d)
            self.lbList.insert(END, ' ')
            i += 1 

    def getInfoObj(self):
        """
        Show detail info from clicked object
        Register a callback to function displayInfoObj
        """
        _obj = str(self.lbList.get(ACTIVE))
        d = getInfoProcessor.getInfo(_obj)
        d.addCallback(self.displayInfoObj)
      
    def displayInfoObj(self, resp):
        """
        Display response object in scrolledbox
        @param resp: respons-object 
        """
        self.stInfo.config(state=NORMAL)
        if resp is None:
            return False
        else:
            self.stInfo.delete(1.0,END)
            self.stInfo.insert(END,resp)
        self.stInfo.config(state=DISABLED)
        
    def setStateOn(self):
        """Set value state on. Call function updateState"""
        self.state['State'] = 'on'
        self.updateState(self.state['State'])
        
    def setStateOff(self):
        """Set value state off. Call function updateState"""
        self.state['State'] = 'off'
        self.updateState(self.state['State'])
        
    def setStateCheck(self):
        """Set value state check. Call function updateState"""
        self.state['State'] = 'check'
        self.updateState(self.state['State'])
        
    def updateState(self, state):
        """
        Call function update from class Function() to send put request
        Register callback for function  displayInfo
        @param state: new state to update 
        """
        _obj = str(self.lbList.get(ACTIVE))
        d = updateProcessor.update(_obj, state)
        d.addCallback(self.displayInfoObj)
        
    def openSubApp(self):
        """Open sub window for task"""
        root = Tk()
        SubApp(root)
    
    def exit(self):
        """Stop reactor, quit programm"""
        reactor.stop()
        
def main():
    """Creat new object root"""
    root = Tk()
    tksupport.install(root)
    App(root)
    
if __name__ == '__main__':
    main()
    reactor.run()