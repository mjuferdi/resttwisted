'''
Created on 16.11.2016

@author: juferdi
'''

from processor import taskProcessor
from twisted.internet import tksupport, reactor
from Tkinter import *
import tkMessageBox
from ScrolledText import ScrolledText

class TaskGui(object):
    """
    Basic Class TaskGui
    
    This class handles Task-API for get information of task data.
    There are entrybox for enter the partition id.
    After partition id is added, click the button GET to execute the request.
    The respons object will show up in scrolltext box. If there is an exception, a message box will pop up.
    """
    def getTask(self):
        """
        Call function getTask() to send a http request. 
        Register a callback to function displayResponse().
        """
        try:
            self.stTask.config(state=NORMAL)
            # Get value from entry box
            _input = self.eParId.get()
            if not _input:
                tkMessageBox.showwarning('Warning', 'Bitte partition id eingeben')
            elif '-' in _input: 
                raise Exception
            else:
                d = taskProcessor.getTask(int(_input))
                d.addCallback(self.displayResponse)
        except:
            tkMessageBox.showwarning('Warning', 'Partition id nicht vorhanden')
            
    def displayResponse(self, resp):
        """
        Display response in scrolltext
        @param resp: response object 
        """
        self.stTask.delete(1.0, END)
        if resp is None:
            self.stTask.config(state=DISABLED)
        else:
            for item in resp:
                self.stTask.insert(END, item+'\n')
        self.stTask.config(state=DISABLED)
        
    def __init__(self, child):
        """"
        Constructor and configuration for all widgets.
        @param child 
        """
        child.title('FlexBB-Task')
        child.resizable(False, False)
        
        # Create a label frame
        lbFrame = LabelFrame(child, text='Task info')
        lbFrame.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky=W+E+S+N)
        
        # Create a label
        lblParId = Label(lbFrame, text='Partition Id:')
        lblParId.grid(row=0, padx=5, pady=5, sticky=W)
        
        # Create an entrybox
        self.eParId = Entry(lbFrame)
        self.eParId.grid(row=0, column=1, padx=5, pady=5, sticky=W+E)
        
        # Create a Button
        btGet = Button(lbFrame, text='GET', command=self.getTask)
        btGet.grid(row=0, column=2, padx=5, pady=5, sticky=W+E)
        
        # Create a scrolltext box
        self.stTask = ScrolledText(lbFrame, width=50, height=8)
        self.stTask.grid(row=1, columnspan=3, padx=5, pady= 7, sticky=W+E+S+N)
        
def main():
    root = Tk()
    tksupport.install(root)
    TaskGui(root)
    
if __name__=='__main__':
    main()
    reactor.run()   