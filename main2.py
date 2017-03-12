import builtwith
import whois
from urllib.request import Request, urlopen
import urllib.parse
import urllib.robotparser
import re
import itertools
import html


#Permite saber que es lo que utiliza la página
#print(builtwith.parse('http://migracion.iniciativa2025alc.org'))
#print(whois.whois('http://migracion.iniciativa2025alc.org'))

def download(url, user_agent='wswp', proxyD=None, num_retries=2):
    print('Descargando url',url)
    headers = {'User-agent':user_agent}
    request = Request(url,headers=headers)
    opener = urllib.request.build_opener()
    if proxyD:
        proxy_params = {urllib.parse.urlparse(url).scheme: proxyD}
        opener.add_handler(urllib.request.ProxyHandler(proxy_params))
    try:
        pagina = urlopen(request).read()
    except Exception as e:
        print('Error:', e)
        pagina = None
        if num_retries > 0:
            if hasattr(e,'code') and 500 <= e.code < 600:
                #Recursivamente intentar errores 5xx HTTP
                return donwload(url,user_agent,proxyD,num_retries-1)
    return pagina

#print(download('http://www.meetup.com/')

def crawl_sitemap(url,user_agent):
    #Descargar el archivo sitemap
    sitemap = download(url,user_agent)
    #extrae los links
    #linkregex = re.compile('<loc>(.*?)</loc>')
    links = re.findall('<loc>(.*?)</loc>',str(sitemap))
    #bajar cada links
    for link in links:
        pagina = download(link)
        #linkH = re.findall('<loc>(.*?)</loc>',str(pagina))
        #crawl_sitemap(linkH[0])

def iterar_example():
    #Cantidad de errores a cometer
    max_errors = 5
    num_errors = 0
    for page in itertools.count(1):
        url = 'http://example.webscraping.com/view/%d' % page
        pagina = download(url,'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16')
        if pagina is None:
            num_errors += 1
            if num_errors == max_errors:
                break
        else:
            # éxito - puedes hacer scraping al resultado
            pass

#iterar_example()
#crawl_sitemap('http://example.webscraping.com/sitemap.xml','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')

def link_crawler(seed_url,link_regex,user_agent,proxyD=None):       
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(seed_url +'/robots.txt')
    rp.read()
    #Crawl from seed_url following links que cumplan el link_regex
    crawl_queue = [seed_url]
    # ver cuales ya han sido visitados
    seen = set(crawl_queue)
    while crawl_queue:
        url = crawl_queue.pop()
        if rp.can_fetch(user_agent,url):
            pagina = download(url,user_agent,proxyD)
            #filtro para links que encajan con el link_regex
            for link in get_links(pagina):
                link = urllib.parse.urljoin(seed_url, link)            
                if re.match(link_regex,link) and link not in seen:
                    seen.add(link)                                               
                    crawl_queue.append(link)
        else:
            print ('Blocked by robots.txt:',url)

def get_links(pagina):
    #Retorna lista de links
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\'](.*?)',re.IGNORECASE)
    #print(webpage_regex.findall(str(html)))
    return webpage_regex.findall(str(html.unescape(pagina)))

#link_crawler('http://example.webscraping.com','http://example.webscraping.com/(index|view)/','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')
link_crawler('http://elcomercio.pe','http://elcomercio.pe/*/','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36','89.163.246.150:8080')
