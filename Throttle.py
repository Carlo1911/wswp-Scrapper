import urllib.parse
import time
from datetime import datetime

class Throttle:
    #Agrega un tiempo entre las descargas de dominio
    def __init__(self,delay):
        #tiempo entre descargas
        self.delay = delay
        #marca de tiempo de cuando se accedio al dominio
        self.domains = {}
    
    def wait(self,url):
        domain = urllib.parse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                #dominio ha sido accedido recientemente
                time.sleep(sleep_secs)
        #actualizar last_accessed
        self.domains[domain] = datetime.now()