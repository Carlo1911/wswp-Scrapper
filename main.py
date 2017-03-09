import builtwith
import whois
from urllib.request import Request, urlopen

#Permite saber que es lo que utiliza la página
print(builtwith.parse('http://migracion.iniciativa2025alc.org'))
print(whois.whois('http://migracion.iniciativa2025alc.org'))

def download(url,num_retries=2):
    print('Descargando url',url)
    try:
        html = urlopen(url).read()
    except Exception as e:
        print('Error:', e)
        html = None
        if num_retries > 0:
            if hasattr(e,'code') and 500 <= e.code < 600:
                #Recursivamente intentar errores 5xx HTTP
                return donwload(url,num_retries-1)
    return html

#print(download('http://httpstat.us/500'))