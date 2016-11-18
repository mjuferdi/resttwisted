'''
Created on 16.11.2016

@author: juferdi
'''

from function import Function
from Tkinter import *
from twisted.internet import tksupport, reactor
import tkMessageBox
from ScrolledText import ScrolledText

class SubApp(object):
    '''
    classdocs
    '''
    def getTask(self):
        try:
            self.stTask.config(state=NORMAL)
            _input = self.eParId.get()
            if not _input:
                tkMessageBox.showwarning('Warning', 'Bitte partition id eingeben')
            elif '-' in _input: 
                raise Exception
            else:
                d = self.fun.task(int(_input))
                d.addCallback(self.displayResponse)
        except:
            tkMessageBox.showwarning('Warning', 'Partition id nicht vorhanden')
            
    def displayResponse(self, resp):
        """Display response in scrolltext"""
        self.stTask.delete(1.0, END)
        if resp is None:
            self.stTask.insert(END, 'Server ist aus')
        else:
            self.stTask.insert(END, resp)
        self.stTask.config(state=DISABLED)
        
    def __init__(self, child):
        """"Konstruktor"""
        self.fun = Function()
        
        child.title('FlexBB-Task')
        lbFrame = LabelFrame(child, text='Task info')
        lbFrame.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky = W+E+S+N)
        
        lblParId = Label(lbFrame, text='Partition Id:')
        lblParId.grid(row=0, padx=5, pady=5, sticky=W)
        
        self.eParId = Entry(lbFrame)
        self.eParId.grid(row=0, column=1, padx=5, pady=5, sticky=W+E)
        
        btGet = Button(lbFrame, text='GET', command=self.getTask)
        btGet.grid(row=0, column=2, padx=5, pady=5, sticky=W+E)
        
        self.stTask = ScrolledText(lbFrame, width=50, height=8)
        self.stTask.grid(row=1, columnspan=3, padx=5, pady= 7, sticky=W+E+S+N)
        
def main():
    root = Tk()
    tksupport.install(root)
    SubApp(root)
    
if __name__=='__main__':
    main()
    reactor.run()   
