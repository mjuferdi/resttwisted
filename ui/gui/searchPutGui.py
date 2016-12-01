'''
Created on 29.11.2016

@author: juferdi
'''

from processor import searchProcessor
from twisted.internet import tksupport, reactor
from Tkinter import *
from ttk import Combobox
from ScrolledText import ScrolledText
import tkMessageBox

class SearchPutGui(object):
    """
    Basic Class SearchPutGui
    
    This class handles Such-API for searching and also updating object in database.
    There are entrybox for enter the object's name to be searched and combobox for new state option.
    After object's name and new state added, click the button PUT below to execute the request.
    The respons object will show up in scrolltext box. If there is an exception, a message box will pop up.
    """
    def __init__(self, child):
        """
        Construktor and configuration for all widgets.
        @param child 
        """
        child.title('FlexBB-Search-PUT')
        child.resizable(False, False)
        
        # Create a label frame
        lbFrame = LabelFrame(child, text='Search-Update')
        lbFrame.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky=W+E+S+N)
         
        # Create a label
        lblName = Label(lbFrame, text='Namen des Objekts:')
        lblName.grid(row=0, padx=5, pady=2, sticky=W)
        
        # Create an entry
        self.eObjName = Entry(lbFrame)
        self.eObjName.grid(row=0, column=1, padx=5, pady=2, sticky=W+S+N)
        
        # Create a label 
        lblState = Label(lbFrame, text='Status: ')
        lblState.grid(row=1, padx=5, sticky=W)
        
        # Create a combobox 
        val = (' ', 'on', 'off', 'check')
        self.cbState = Combobox(lbFrame, values=val)
        self.cbState.current(0)
        self.cbState.grid(row=1, column=1, padx=5, pady=5, sticky=W)
        
        # Create a button
        btPut = Button(lbFrame, text='PUT', command=self.putSearchObject)
        btPut.grid(row=3, column=0, columnspan=1, padx=5, pady=5, sticky=W+E+S+N)
        
        # Create a scrolltext box
        self.stInfo = ScrolledText(lbFrame, width=25, height=10)
        self.stInfo.grid(row=4, columnspan=2, padx=5, pady=5, sticky=W+E)
        
    def putSearchObject(self):
        """
        Value from entrybox and combobox are being used for the function parameter from getSearchUpdate().
        Register a callback to function displayResponse().
        """
        # Get value from entrybox
        _input = self.eObjName.get()
        # Get value from combobox
        status = self.cbState.get()
        # If the entrybox is empty, show this messagebox
        if not _input:
            tkMessageBox.showinfo('', 'Bitte Name des Such-Objekts eingeben')
        # If the entrybox is not empty, register a callback. 
        elif len(_input) != 0:
            d = searchProcessor.getSearchUpdate(_input, status, partition=None)
            d.addCallback(self.displayResponse)
            
    def displayResponse(self, resp):
        """
        Show the return value and put it in scrolltext.
        @param resp: Respon-Object 
        """
        self.stInfo.config(state=NORMAL)
        self.stInfo.delete(1.0, END)
        if resp is None:
            return False
        else:
            self.stInfo.insert(END, resp)
            self.stInfo.config(state=DISABLED)
            
def main():
    """create new object as parameter for class SearchPutGui"""
    root = Tk()
    tksupport.install(root)
    SearchPutGui(root)
    
if __name__=='__main__':
    main()
    reactor.run()