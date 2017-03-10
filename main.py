import builtwith
import whois
from urllib.request import Request, urlopen
import re

#Permite saber que es lo que utiliza la página
#print(builtwith.parse('http://migracion.iniciativa2025alc.org'))
#print(whois.whois('http://migracion.iniciativa2025alc.org'))

def download(url, user_agent='wswp', num_retries=2):
    print('Descargando url',url)
    headers = {'User-agent':user_agent}
    request = Request(url,headers=headers)
    try:
        html = urlopen(request).read()
    except Exception as e:
        print('Error:', e)
        html = None
        if num_retries > 0:
            if hasattr(e,'code') and 500 <= e.code < 600:
                #Recursivamente intentar errores 5xx HTTP
                return donwload(url,num_retries-1)
    return html

#print(download('http://www.meetup.com/')

def crawl_sitemap(url,user_agent):
    #Descargar el archivo sitemap
    sitemap = download(url,user_agent)
    #extrae los links
    #linkregex = re.compile('<loc>(.*?)</loc>')
    links = re.findall('<loc>(.*?)</loc>',str(sitemap))
    #bajar cada links
    for link in links:
        html = download(link)
        #linkH = re.findall('<loc>(.*?)</loc>',str(html))
        #crawl_sitemap(linkH[0])

crawl_sitemap('http://elcomercio.pe/sitemap2.xml','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')