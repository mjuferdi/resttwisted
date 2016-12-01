#-*- coding: utf-8 -*-

"""
Created on 16.11.2016

@author: juferdi
"""

from processor import pingProcessor, searchProcessor, getInfoProcessor, updateProcessor
from gui import taskGui, searchPutGui
from Tkinter import *
from twisted.internet import reactor
from ScrolledText import ScrolledText
from ttk import Combobox
import tkMessageBox

class App(object):
    """
    Basic Class App
    
    This is the main graphical user interface. In this class there us a button 'Check Server' 
    to check the connection to the server. Click the button 'Get Liste' to send a GET-request,
    if the connection is connected to the server, the server will send response in the form of a list 
    of all the object's name, that will be displayed on the listbox. 
    
    Select one or more objects from the listbox, and click the 'GET' button on 
    the right side, to see more information about the object. The three buttons below 
    serves to update the status of the object.
    
    Button 'Task' and 'Search-PUT' have the funtion to open a new window.
    Click button 'Beenden' to stop the reactor and close the program.
    """
    def __init__(self, master):
        """
        Konstruktor and configuration for all widgets.
        """
        self.resp = []
        self.listname = []
        self.state = {'State':''}
        master.title('FlexBB')
        master.rowconfigure(0, weight=1)
        master.columnconfigure(0, weight=1)
        master.resizable(False, False)
        
        # Create labelframe left side
        lfLeft = LabelFrame(master, text='Melder-Liste')
        lfLeft.grid(row=0, column=0, columnspan=4, sticky=W+N+S,
                    padx=5, pady=5, ipadx=5, ipady=5)
        
        # Create label search
        lbSearch = Label(lfLeft, text='Geben Sie Melder-Name ein :')
        lbSearch.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        
        # Create combobox
        opt = ('Sortiere nach:', 'Flexzone', 'Element type')
        self.cbSort = Combobox(lfLeft, values=opt, state='readonly')
        self.cbSort.current(0)
        self.cbSort.bind('<<ComboboxSelected>>', self.displayListObj)
        self.cbSort.grid(row=3, padx=5, sticky=W)
        self.cbSort.config(state=DISABLED)
        
        # Create entrybox
        self.eSearch = Entry(lfLeft)
        self.eSearch.grid(row=0, column=1, padx=5, pady=2)
        self.eSearch.config(state=DISABLED)
        
        # Create button search
        self.btSearch = Button(lfLeft, text='Get Liste', command=self.getList)
        self.btSearch.grid(row=0, column=2, padx=5, pady=2)
        
        # Create scrollbar
        sb = Scrollbar(lfLeft)
        sb.grid(row=4, column=3, pady=5, sticky=N+S)
        
        # Create listbox
        self.lbList = Listbox(lfLeft, selectmode='multiple', yscrollcommand=sb.set, height=20)
        self.lbList.grid(row=4, columnspan=3, padx=5, pady=5, sticky=W+E)
        sb.config(command=self.lbList.yview)
        
        # Create labelframe right side
        self.lfRight = LabelFrame(master, text='Information')
        self.lfRight.grid(row=0, column=6, sticky=N+S, padx=5, pady=5, ipadx=5, ipady=5)
        
        # Create scrolltext info
        self.stInfo = ScrolledText(self.lfRight, width=35, height=10)
        self.stInfo.grid(row=0, columnspan=3, padx=5, sticky=W+E)
        
        # Create button check server
        btIsAlive = Button(self.lfRight, text='Check Server', command=pingProcessor.getPing)
        btIsAlive.grid(row=5, padx=5, pady=5, sticky=W+E)
        
        # Create button GET
        self.btGet = Button(self.lfRight, text='GET', command=lambda: self.registerCallback('getinfo', None))
        self.btGet.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=W+E)
        self.btGet.config(state=DISABLED)
        
        # Create button Clear
        self.btClear = Button(self.lfRight, text='Löschen', command=self.clearStInfo)
        self.btClear.grid(row=1, column=2, padx=5, pady=5, sticky=W+E)
        
        # Create button on
        btOn = Button(self.lfRight, text='ON', command=lambda: self.registerCallback('getUpdate', 'on'))
        btOn.grid(row=2, columnspan=3, padx=5, pady=5, sticky=W+E)
        
        # Create button off
        btOff = Button(self.lfRight, text='OFF', command=lambda: self.registerCallback('getUpdate', 'off'))
        btOff.grid(row=3, columnspan=3, padx=5, pady=5, sticky=W+E)
        
        # Create button check
        btCheck = Button(self.lfRight, text='CHECK', command=lambda: self.registerCallback('getUpdate', 'check'))
        btCheck.grid(row=4, columnspan=3, padx=5, pady=5, sticky=W+E)
        
        # Create button task
        btTask = Button(self.lfRight, text='Task', command=lambda: self.openChildUi('task'))
        btTask.grid(row=5, column=1, padx=5, pady=5, sticky=W+E)
        
        # Create button searchput
        btSearchPut = Button(self.lfRight, text='Search-PUT', command=lambda: self.openChildUi('searchput'))
        btSearchPut.grid(row=5, column=2, padx=5, pady=5, sticky=W+E)
        
        # Create button beenden
        btExit = Button(self.lfRight, text='Beenden', command=self.exit)
        btExit.grid(row=6, padx=5, pady=5, sticky=W)
        
    def getList(self):
        """
        Show all object and/or search given object's name, then put in listbox.
        To get list of objects from database, it needs to call function getList().
        Register a callback to function setNewList() to create list, that contains only the name of object.
        """
        self.btSearch['text'] = 'Suche'
        self.eSearch.config(state=NORMAL)
        self.btGet.config(state=NORMAL)
        self.cbSort.config(state=NORMAL)
        self.lbList.delete(0, END)
        # Get the value from entrybox
        _input = self.eSearch.get()
        if not _input:
            d = searchProcessor.getList()
            d.addCallback(self.setNewList)
        elif len(_input) != 0:
            # Search of string object name in a list of strings
            # If object's name isn't in the list, show the message box
            matching = [s for s in self.listname if _input in s]
            if len(matching) != 0:
                for item in matching:
                    self.lbList.insert(END, item)
            else:
                tkMessageBox.showinfo('', 'Der Name "%s" ist nicht vorhanden' % _input)
             
    def setNewList(self, resp):
        """
        Set global variable resp.
        Create new list contains only name.
        @param resp: respons-object 
        """
        self.resp = resp
        if resp is None:
            return resp
        else:
            # Create a new list using the function map() to get the value with key 'name' 
            self.listname = map(lambda d: d['name'], self.resp)
        self.displayListObj(self.resp)
        
    def displayListObj(self, resp):
        """
        Display response object in listbox. The list can be sorted by selecting options in the combobox.
        After the option is selected, the function sortList() is called.
        @param resp: response object 
        """
        try:
            resp = self.resp
            # Get the value from combobox
            value = self.cbSort.get()
            self.stInfo.config(state=NORMAL)             
            self.stInfo.delete(1.0, END)
            self.lbList.delete(0,END)
            if value == 'Sortiere nach:':
                for item in resp:
                    self.lbList.insert(END, item['name'])
            elif value == 'Flexzone':
                self.sortList(int(0), 'flexzoneid', 9, 'Flexzone id ')
            elif value == 'Element type':
                self.sortList(int(1), 'elementtype', 3, 'Element type ')
        except:
            return None
    
    def sortList(self, par, key, ran, text):
        """
        Sort the list with function sorted().
        @param par: int index parameter
        @param key: key in list of dict
        @param ran: range for do looping
        @param text: output text   
        """
        i = par
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
    
    def registerCallback(self, func, state=None):
        """
        Register a callback to function displayInfoObj() by parameter func.
        @param func: method request
        @param state: new state to be updated.
        """
        selectedObj = self.lbList.curselection()
        objarr = []
        for i in selectedObj:
            _obj = str(self.lbList.get(i))
            objarr.append(_obj)
        if func == 'getinfo':
            d = getInfoProcessor.getInfo(objarr)
        elif func == 'getUpdate' and state is not None:
            d = updateProcessor.getUpdate(objarr, state)
        d.addCallback(self.displayInfoObj)  
      
    def displayInfoObj(self, resp):
        """
        Display response object in scrolledtext box.
        @param resp: respons-object 
        """
        self.stInfo.config(state=NORMAL)
        if resp is None:
            return False
        else:
            self.stInfo.delete(1.0,END)
            for i in resp:
                self.stInfo.insert(END,i+'\n')
            self.stInfo.config(state=DISABLED)
        
    def clearStInfo(self):
        """Clear scrolltext and set the box to readonly."""
        self.stInfo.config(state=NORMAL)
        self.stInfo.delete(1.0, END)
        self.stInfo.config(state=DISABLED)
        self.lbList.select_clear(0, END)
    
    def openChildUi(self, req):
        """
        Open sub window.
        @param req: selection window
        """
        root = Tk()
        if req == 'task':
            taskGui.TaskGui(root)
        elif req == 'searchput':
            searchPutGui.SearchPutGui(root)
            
    def exit(self):
        """Stop reactor and quit program"""
        reactor.stop()