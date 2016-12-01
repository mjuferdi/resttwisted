#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
The graphical user interface for FlexBB REST Client API

The GUI consists of three windows: main window, task-editor and search-put-editor. 
Each window has widgets with different functions that are implemented with REST Client API.
The GUI created with Tkinter package. To integrate GUI and Twisted reactor from API, it needs
to import module tksupport from twisted.internet.
"""

from gui import mainGUI
from Tkinter import Tk
from twisted.internet import reactor, tksupport

def main():
    """
    Build Tk app using the root object
    Start the programm with reactor.run(), and stop it
    with reactor.stop(). 
    """
    root = Tk()
    # Install the Reactor support.
    tksupport.install(root)
    mainGUI.App(root)
    
if __name__ == '__main__':
    main()
    reactor.run() 
