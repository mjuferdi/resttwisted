#-*- coding: utf-8 -*-

'''
Created on 16.11.2016

@author: juferdi
'''
from function import Function
from childui import SubApp
from Tkinter import *
from twisted.internet import reactor, tksupport
from ScrolledText import ScrolledText
import tkMessageBox

class App(object):
    """Basic Class App"""
    def ping(self):
        """Register a callback to msgbox function"""
        d = self.fun.ping()
        d.addCallback(self.msgbox)
        
    def msgbox(self,resp):
        """
        Show messagebox contain response
        @param resp: response object 
        """
        tkMessageBox.showinfo('IsAlive', resp)
    
    def exit(self):
        """Stop reactor, quit programm"""
        reactor.stop()
        
    def searchObj(self):
        """Show all object or search given object's name and put in listbox"""
        self.lfRight['text'] = 'Info'
        self.btSearch['text'] = 'Search'
        self.eSearch.config(state=NORMAL)
        self.btGet.config(state=NORMAL)
        self.lbList.delete(0, END)
        _input = self.eSearch.get()
        if not _input:
            d = self.fun.getList()
            d.addCallback(self.displayObj)
        elif _input in self.resp:
            self.lbList.insert(END,_input)
        elif _input not in self.resp:
            tkMessageBox.showinfo('', 'No name for "%s"' % _input)
            
    def displayObj(self, resp):
        """display response object in listbox"""
        self.resp = resp
        try:
            self.stInfo.config(state=NORMAL)
            self.stInfo.delete(1.0, END)
            self.lbList.delete(0,END)
            for item in resp:
                self.lbList.insert(END, item)
        except:
            return None
    
    def infoObj(self):
        """show detail info from clicked object"""
        _obj = str(self.lbList.get(ACTIVE))
        self.lfRight['text'] = 'Info ' + _obj 
        d = self.fun.searchName(_obj)
        d.addCallback(self.displayInfo)
      
    def displayInfo(self, resp):
        """display response object in scrolledbox"""
        self.stInfo.config(state=NORMAL)
        self.stInfo.delete(1.0,END)
        self.stInfo.insert(END,resp)
        self.stInfo.config(state=DISABLED)
        
    def stateOn(self):
        """Set value state on. Call function updateState"""
        self.state['State'] = 'on'
        self.updateState()
        
    def stateOff(self):
        """Set value state off. Call function updateState"""
        self.state['State'] = 'off'
        self.updateState()
        
    def stateCheck(self):
        """Set value state check. Call function updateState"""
        self.state['State'] = 'check'
        self.updateState()
        
    def updateState(self):
        """
        Call function update from class Function() to send put request
        Register callback for function  displayInfo
        """
        _obj = str(self.lbList.get(ACTIVE))
        self.lfRight['text'] = 'Info ' + _obj
        d = self.fun.update(_obj, self.state['State'])
        d.addCallback(self.displayInfo)
        
    def openSubApp(self):
        """Open sub window for task"""
        root = Tk()
        SubApp(root)
            
    def __init__(self, master):
        """
        Konstruktor
        """
        self.fun = Function()
        self.resp = []
        self.state = {'State':''}
        
        
        master.title('FlexBB')
        # setup labelframe1
        lfLeft = LabelFrame(master, text='Object list')
        lfLeft.grid(row=0, column=0, columnspan=4, sticky=W,
                    padx=5, pady=5, ipadx=5, ipady=5)
        
        sb = Scrollbar(lfLeft)
        sb.grid(row=3, column=3, pady=5, sticky=W+E+N+S)
        
        lbSearch = Label(lfLeft, text='Enter object name to be searched:')
        lbSearch.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        
        self.eSearch = Entry(lfLeft)
        self.eSearch.grid(row=0, column=1, padx=5, pady=2)
        self.eSearch.config(state=DISABLED)
        
        self.btSearch = Button(lfLeft, text='Get List', command=self.searchObj)
        self.btSearch.grid(row=0, column=2, padx=5, pady=2)
        
        self.lbList = Listbox(lfLeft, yscrollcommand=sb.set, width=40, height=20)
        self.lbList.grid(row=3, columnspan=3, pady=5, sticky=W+E)
        sb.config(command=self.lbList.yview)
        
        # setup labelframe2
        self.lfRight = LabelFrame(master, text='Info')
        self.lfRight.grid(row=0, column=6, sticky=N+S, padx=5, pady=5, ipadx=5, ipady=5)
        
        self.stInfo = ScrolledText(self.lfRight, width=35, height=10)
        self.stInfo.grid(row=0, column=0, columnspan=3, padx=5, sticky=W+E)
            
        btIsAlive = Button(self.lfRight, text='Check Server', command=self.ping)
        btIsAlive.grid(row=5, column=0, columnspan=1, padx=5, pady=5, sticky=W+E)
        
        self.btGet = Button(self.lfRight, text='GET', command=self.infoObj)
        self.btGet.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky=W+E)
        self.btGet.config(state=DISABLED)
        
        btOn = Button(self.lfRight, text='ON', command=self.stateOn)
        btOn.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky=W+E)
        
        btOff = Button(self.lfRight, text='OFF', command=self.stateOff)
        btOff.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky=W+E)
        
        btCheck = Button(self.lfRight, text='CHECK', command=self.stateCheck)
        btCheck.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky=W+E)
        
        btTask = Button(self.lfRight, text='Task', command=self.openSubApp)
        btTask.grid(row=5, column=1, columnspan=2, padx=5, pady=5, sticky=W+E)
        
        btExit = Button(self.lfRight, text='Exit', command=self.exit)
        btExit.grid(row=6, padx=5, pady=5, sticky=W)
    
def main():
    root = Tk()
    tksupport.install(root)
    App(root)
    
if __name__ == '__main__':
    main()
    reactor.run()
