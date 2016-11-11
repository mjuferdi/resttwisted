# -*- coding: utf-8 -*-

"""
Created on 01.11.2016

@author: juferdi
"""

import matplotlib.pyplot as plt
import pylab

class Config():
    """
    Basic Config class
    """
    def help(self):
        """
        Open file help.txt to get information about function.
        """
        text = open('help.txt', 'r')
        textContent = text.read()
        print (textContent)
        text.close()
        exit()
        
    def errorHandling(self):
        """
        Error and exceptions handling.
        """
        print 'USAGE: main.py [command + func] [option]'
        print 'The command is either wrong type or could not be found.'
        print 'Type -h or --help for more information.'
        exit()
    
    def setPlot(self,q,isThread):
        """
        Create Chart.
        @param q: list of values for drawing Chart.
        @param isThread: to check, whether the function in parallel. 
        """
        if isThread is True and len(q) > 1:
            a = 0
            listLat = []
            listSec = []
            for i in xrange(len(q)):
                listLat += q[a][0]
                listSec += q[a][2]
                plt.plot(q[a][1], q[a][0], label="Thread-%s" % str(i+1), linewidth = 1.5)
                a += 1
            plt.axis([0, max(listSec), 0, max(listLat)+10])
            plt.legend(loc='upper right')
        else:
            x = q[0][1]
            y = q[0][0]
            z = q[0][2]
            plt.plot(x, y, linewidth=1.5)
            plt.axis([0, max(z), 0, max(y)+10])
        plt.ylabel('Latency in ms')
        plt.xlabel('Second elapsed')
        plt.title('Load Curve')
        plt.grid(True)
        pylab.show()