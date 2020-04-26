import requests as s
import sys
from lxml import html
from lxml.html import fromstring
from itertools import cycle
import traceback

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
    #-----------------------------------------------------------------------------------------------------
    proxies = get_proxies()
    proxy_pool = cycle(proxies)
    proxy = next(proxy_pool)

    #------------------------------------------------------------------------------------------------------
    url = 'https://www.cruzverde.com.co/search?q=' + medicamento + "&search-button=&lang=es_CO"
    
    pagina = s.get(url, proxies={"http": proxy}, timeout=5)
    print(url, proxies)
    try:
        if pagina.status_code == 200:
            pagina.encoding = 'ISO-8859-1'
            txtHtml = html.fromstring(pagina.content)
            urlPAGS = txtHtml.xpath("//span[@class='text-uppercase pagination-text']/text()")
            fichaTec = txtHtml.xpath("//span[@class='tab1Title']/text()")
            sinResultados = txtHtml.xpath("//p[@class='no-results-message text-center']/text()")
            pagina = 0
            #print(sinResultados)
            try:
                if sinResultados == []:
                    #Cuando hay varias paginas
                    if urlPAGS != [] :
                        for pagina in range(50):
                            print(pagina + 1)
                            pagina= pagina*12  
                            url2 = 'https://www.cruzverde.com.co/search?q=' + medicamento + "&search-button=&lang=es_CO&start=" + str(pagina) +"&sz=12"
                            #print(url2)
                            pagina2 = s.get(url2, proxies={"http": proxy }, timeout=5)
                            print(url2, proxies)
                            txtHtml2 = html.fromstring(pagina2.content)
                            sinResultados2 = txtHtml2.xpath("//p[@class='no-results-message text-center']/text()")
                            #print(sinResultados2)
                            #print(url2)

                            if sinResultados2 == []:
                                nombres = txtHtml2.xpath("//a[@class='link']/text()")
                                precios = txtHtml2.xpath("//span[@class='value pr-2']/text()")
                                for n,p in zip(nombres,precios):
                                    n= n.replace("\n        \n            ", "")
                                    n= n.replace("\n        \n    ", "")
                                    p= p.replace("\n                    ", "")
                                    p= p.replace("\n                ", "")
                                    print(n +":"+p) 
                            else :
                                break    

                    #cuando solo hay un medicamnto
                    elif fichaTec != []:

                        nombres = txtHtml.xpath("//h1[@class='product-name']/text()")
                        precios = txtHtml.xpath("//span[@class='value pr-2']/text()")
                        nombres[0] =nombres[0].replace("\n        \n            ", "")
                        nombres[0] =nombres[0].replace("\n        \n    ", "")
                        precios[0] = precios[0].replace("\n                    ", "")
                        precios[0] = precios[0].replace("\n                ", "")
                
                        print(nombres[0] + ":"+ precios[0] )

                    #cuando hay solo una pagina
                    elif fichaTec == []:
                        nombres = txtHtml.xpath("//a[@class='link']/text()")
                        precios = txtHtml.xpath("//span[@class='value pr-2']/text()")
                        for n,p in zip(nombres,precios):
                            n= n.replace("\n        \n            ", "")
                            n= n.replace("\n        \n    ", "")
                            p= p.replace("\n                    ", "")
                            p= p.replace("\n                ", "")
                            print(n +":"+p)
                else:
                    print(sinResultados[0])
            
            except:
                print("Error")
                          
        else:
            print("Error al cargar la pagina")


    except:
        print("Error al cargar la pagina")

            

if __name__ == '__main__':
   main(sys.argv[1])


