'''
Created on 29.09.2016

@author: juferdi
'''
from twisted.internet import reactor
from CheckConnection import Check
from FindDetector import FindDetector

def test():
    try:
        method = raw_input('Method (GET/PUT):',)
        if method == 'GET' or method == 'get':
            anf = raw_input('GET (PING, NAME, STATUS):',)
            if anf == 'PING' or anf == 'ping':
                main = Check()
                main.call()
            elif anf == 'NAME' or anf == 'name':
                name = raw_input('bitte name eingeben: ',)
                main = FindDetector(name)
                main.search()
            elif anf == 'STATUS' or anf == 'status':
                name = raw_input('bitte name eingeben: ',)
                main = FindDetector(name)
                main.review()
            else:
                print 'Request nicht vorhanden'
        elif method == 'PUT' or method == 'put':
            req = raw_input('bitte name eingeben: ',)
            main = FindDetector(req)
            state = raw_input('state eingeben: ',)
            main.update(state)
        else:
            print 'Method nicht zugelassen'
    except:
        pass
    finally:
        pass
    
test()    
reactor.run() 
