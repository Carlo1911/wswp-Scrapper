import builtwith
import whois
from urllib.request import Request, urlopen
import urllib.parse
import urllib.robotparser
import re
import itertools
from Throttle import Throttle
from multiprocessing import Queue
import html

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
                return download(url,user_agent,proxyD,num_retries-1)
    return pagina

def crawl_sitemap(url,user_agent):
    #Descargar el archivo sitemap
    sitemap = download(url,user_agent)
    #extrae los links
    #linkregex = re.compile('<loc>(.*?)</loc>')
    links = re.findall('<loc>(.*?)</loc>',str(sitemap))
    #bajar cada links
    for link in links:
        pagina = download(link)

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
            num_errors = 0

def get_robots(url):
    #Initialize robots parser for this domain
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(urllib.parse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp

def link_crawler(seed_url,link_regex,user_agent,proxyD=None, headers=None, num_retries=1, delay=2,max_depth=-1, max_urls=-1):    
    rp = get_robots(seed_url)
    #Crawl from seed_url following links que cumplan el link_regex
    crawl_queue = Queue(0)
    crawl_queue.put(seed_url)
    # the URL's that have been seen and at what depth
    seen = {seed_url: 0}
    num_urls = 0

    throttle = Throttle(delay)
    headers = headers or {}
    if user_agent:
        headers['User-agent'] = user_agent

    while crawl_queue:
        url = crawl_queue.get()
        if rp.can_fetch(user_agent,url):
            throttle.wait(url)
            pagina = download(url,user_agent,proxyD, num_retries)
            links = []
            depth = seen[url]
            if depth != max_depth:                
                links = get_links(pagina)
                #filtro para links que encajan con el link_regex
                for link in links:
                    link = normalize(seed_url, link)  
                    if link not in seen and re.match(link_regex, link):
                        seen[link] = depth + 1
                        if same_domain(seed_url, link):
                            # success! add this new link to queue
                            crawl_queue.put(link)
            # check whether have reached downloaded maximum
            num_urls += 1
            if num_urls == max_urls:
                break
        else:
            print ('Blocked by robots.txt:',url)

def same_domain(url1, url2):
    """Return True if both URL's belong to same domain
    """
    return urllib.parse.urlparse(url1).netloc == urllib.parse.urlparse(url2).netloc

def normalize(seed_url, link):
    """Normalize this URL by removing hash and adding domain
    """
    link = urllib.parse.urldefrag(link[0]) # return DefragResult(url='http://publimetro.pe/?ref=ecf', fragment='')
    return urllib.parse.urljoin(seed_url, link[0])

def get_links(pagina):
    #Retorna lista de links
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\'](.*?)',re.IGNORECASE)
    pagina = html.unescape(str(pagina))
    return webpage_regex.findall(str(pagina))


#Permite saber que es lo que utiliza la página
#print(builtwith.parse('https://codigofacilito.com/'))
#print(whois.whois('http://migracion.iniciativa2025alc.org'))

link_crawler('https://codigofacilito.com','https://codigofacilito.com/*/','archive.org_bot','89.163.246.150:8080',delay=1)
