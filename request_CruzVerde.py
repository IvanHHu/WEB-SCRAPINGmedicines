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

    #-----------------------------------------------------------------------------------------------------
    proxies = get_proxies()
    proxy_pool = cycle(proxies)
    proxy = next(proxy_pool)

    #------------------------------------------------------------------------------------------------------
    url = 'https://www.cruzverde.com.co/search?q=' + medicamento + "&search-button=&lang=es_CO"
    
    try:
        pagina = s.get(url, proxies={"http": proxy},headers=headers, timeout=5)
        #print(url, proxies, headers)
        print(url)
        if pagina.status_code == 200:
            try:
                pagina.encoding = 'ISO-8859-1'
                txtHtml = html.fromstring(pagina.content)
                urlPAGS = txtHtml.xpath("//span[@class='text-uppercase pagination-text']/text()")
                fichaTec = txtHtml.xpath("//span[@class='tab1Title']/text()")
                sinResultados = txtHtml.xpath("//p[@class='no-results-message text-center']/text()")
                pagina = 0
                #print(sinResultados)
                if sinResultados == []:
                    #Cuando hay varias paginas
                    if urlPAGS != [] :
                        try:
                            for pagina in range(50):
                                print(pagina + 1)
                                pagina= pagina*12  
                                url2 = 'https://www.cruzverde.com.co/search?q=' + medicamento + "&search-button=&lang=es_CO&start=" + str(pagina) +"&sz=12"
                                pagina2 = s.get(url2, proxies={"http": proxy },headers=headers, timeout=5)
                                #print(url2, proxies, headers)
                                print(url2)
                                txtHtml2 = html.fromstring(pagina2.content)
                                sinResultados2 = txtHtml2.xpath("//p[@class='no-results-message text-center']/text()")
                                #print(sinResultados2)
                                #print(url2)

                                if sinResultados2 == []:
                                    jsonList = []
                                    nombres1 = []
                                    precios1 = []
                                    nombres = txtHtml2.xpath("//a[@class='link']/text()")
                                    precios = txtHtml2.xpath("//span[@class='value pr-2']/text()")

                                    for i in range(0,len(nombres)):
                                        nombres[i] = nombres[i].replace("\n        \n            ", "")
                                        nombres[i] = nombres[i].replace("\n        \n    ", "")
                                        precios[i] = precios[i].replace("\n                    ", "")
                                        precios[i] = precios[i].replace("\n                ", "")
                                        nombres1.append(nombres[i])
                                        precios1.append(precios[i])
                                    #print(nombres1)

                                    for i in range(0,len(nombres)):
                                        jsonList.append({"medicamento" : nombres[i], "precio" : precios[i]})
                                    
                                    print(json.dumps(jsonList, indent = 1))
  
                                else :
                                    break
                            return 0
                        except:
                            print("La request tiene bastantes productos y fallo en esta sección")
                            return -3
                    #cuando solo hay un medicamento
                    elif fichaTec != []:
                        try:
                            jsonList = []
                            nombres1 = []
                            precios1 = []
                            nombres = txtHtml.xpath("//h1[@class='product-name']/text()")
                            precios = txtHtml.xpath("//span[@class='value pr-2']/text()")

                            for i in range(0,len(nombres)):
                                nombres[i] = nombres[i].replace("\n        \n            ", "")
                                nombres[i] = nombres[i].replace("\n        \n    ", "")
                                precios[i] = precios[i].replace("\n                    ", "")
                                precios[i] = precios[i].replace("\n                ", "")
                                nombres1.append(nombres[i])
                                precios1.append(precios[i])

                            for i in range(0,len(nombres)):
                                jsonList.append({"medicamento" : nombres[i], "precio" : precios[i]})
                                    
                            print(json.dumps(jsonList, indent = 1))
                           
                            return 0
                        except:
                            print("La request tiene tiene entre 2 y 12 productos y fallo en esta sección")
                            return -2
                    #cuando hay solo una pagina
                    elif fichaTec == []:
                        try:
                            jsonList = []
                            nombres1 = []
                            precios1 = []
                            nombres = txtHtml.xpath("//a[@class='link']/text()")
                            precios = txtHtml.xpath("//span[@class='value pr-2']/text()")

                            for i in range(0,len(nombres)):
                                nombres[i] = nombres[i].replace("\n        \n            ", "")
                                nombres[i] = nombres[i].replace("\n        \n    ", "")
                                precios[i] = precios[i].replace("\n                    ", "")
                                precios[i] = precios[i].replace("\n                ", "")
                                nombres1.append(nombres[i])
                                precios1.append(precios[i])
                            
                            for i in range(0,len(nombres)):
                                jsonList.append({"medicamento" : nombres[i], "precio" : precios[i]})
                                    
                            print(json.dumps(jsonList, indent = 1))

                        except:
                            print("La request tiene un producto y fallo en esta sección")
                            return -1
                else:
                    print(sinResultados[0])
            
            except:
                print("La petición hecha no fue exitosa")
                return 3
                          
        else:
            print("El request fue exitoso, mas algo paso en la pagina")
            return 2


    except:
        print("Error desconocido al iniciar la petición")
        return 1

            

if __name__ == '__main__':
  status =  main(sys.argv[1])
  print(status)
