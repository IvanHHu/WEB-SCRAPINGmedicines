import requests as s
import sys
from lxml import html
from lxml.html import fromstring
from itertools import cycle
import traceback
import random
import json



def main(medicamento):
    def get_proxies():
        url = 'https://free-proxy-list.net/'
        response = s.get(url)
        parser = fromstring(response.text)
        proxies = set()
        for i in parser.xpath('//tbody/tr')[:10]:
            if i.xpath('.//td[7][contains(text(),"yes")]'):
                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                proxies.add(proxy)
        return proxies
    
    #----------------------------------------------------------------------------------------------------
    user_agent_list = [
    #Chrome
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        #Firefox
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
    ]
    user_agent = random.choice(user_agent_list)
    #Set the headers 
    headers = {'User-Agent': user_agent}

    #----------------------------------------------------------------------------------------------------------
    proxies = get_proxies()
    proxy_pool = cycle(proxies)
    proxy = next(proxy_pool)

    pag = 0
    for pagina in range(50):
        pag= pag + 1 
        url = "https://www.locatelcolombia.com/buscapagina?ft=" + medicamento + "&PS=12&sl=e3672a70-87b5-474e-b217-cea662d2e462&cc=1&sm=0&PageNumber="+ str(pag)
        print(pag)
        try:
            pagina = s.get(url, proxies={"http": proxy},headers=headers, timeout=5)
            print(url, proxies,headers)
            if pagina.status_code == 200:
                try:
                    pagina.encoding = 'ISO-8859-1'
                    if str(pagina.content) != "b''":
                        try:
                            txtHtml = html.fromstring(pagina.content)
                            sinResultados = txtHtml.xpath("//div[@class='page-title']//h2/text()")

                            if sinResultados == []:
                                jsonList = []
                                precios1 = []
                                nombres = txtHtml.xpath("//a[@class='product-name']/text()")
                                precios = txtHtml.xpath("//span[@class='bestPrice']/text()")
                                
                                for i in range(0,len(precios)):
                                    precios[i] = precios[i].replace("\n                ", "")
                                    precios[i] = precios[i].replace("\n            ", "")
                                    precios1.append(precios[i])

                                for i in range(0,len(precios)):
                                    jsonList.append({"medicamento" : nombres[i], "precio" : precios[i]})
                                
                                print(json.dumps(jsonList, indent = 1))

                            else:
                                print(sinResultados[0] + "... No hay esultados")
                                return 0
                        except:
                            print("La request tiene bastantes productos y fallo en esta sección")
                            return -3

                    elif str(pagina.content) == "b''":
                        #print(pagina.content)
                        break
                except:
                    print("La petición hecha no fue exitosa")
                    return 3
                
            else:
                print("Error al cargar la pagina")
                return 2
        except:
            print("Error desconocido al iniciar la petición")
            return 1
            
             

if __name__ == '__main__':
    status =  main(sys.argv[1])
    print(status)
