import requests as s
from bs4 import BeautifulSoup
import sys
from lxml import html
from lxml.html import fromstring
from itertools import cycle
import traceback
import random

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


    url = "https://www.drogueriascafam.com.co/buscar?search_query=" + medicamento + "&controller=search&orderby=position&orderway=desc"
    try:
        pagina = s.get(url,proxies={"http": proxy},headers=headers, timeout=5)
        print(url, proxies, headers)
        if pagina.status_code == 200:
            try:
                pagina.encoding = 'ISO-8859-1'
                txtHtml = html.fromstring(pagina.content)
                sinResultados = txtHtml.xpath("//p[@class='alert alert-warning']/text()")
                print(sinResultados)

                if sinResultados ==[]:

                    indPag = txtHtml.xpath("//div[@class='clearfix selector1']/span[1]/text()")
                    print (indPag)
                    if indPag == []:
                        try:
                            nombres = txtHtml.xpath("//span[@class='grid-name']/text()")
                    
                            prec1 = txtHtml.xpath("//div[@class='columns-container']//li[1]//div[1]//div[2]//span[1]/text()")
                            prec2 = txtHtml.xpath("//div[@class='columns-container']//li[2]//div[1]//div[2]//span[1]/text()")
                            prec3 = txtHtml.xpath("//div[@class='columns-container']//li[3]//div[1]//div[2]//span[1]/text()")
                            prec4 = txtHtml.xpath("//div[@class='columns-container']//li[4]//div[1]//div[2]//span[1]/text()")
                            prec5 = txtHtml.xpath("//div[@class='columns-container']//li[5]//div[1]//div[2]//span[1]/text()")
                            prec6 = txtHtml.xpath("//div[@class='columns-container']//li[6]//div[1]//div[2]//span[1]/text()")
                            prec7 = txtHtml.xpath("//div[@class='columns-container']//li[7]//div[1]//div[2]//span[1]/text()")
                            prec8 = txtHtml.xpath("//div[@class='columns-container']//li[8]//div[1]//div[2]//span[1]/text()")
                            prec9 = txtHtml.xpath("//div[@class='columns-container']//li[9]//div[1]//div[2]//span[1]/text()")
                            prec10 = txtHtml.xpath("//div[@class='columns-container']//li[10]//div[1]//div[2]//span[1]/text()")
                            prec11 = txtHtml.xpath("//div[@class='columns-container']//li[11]//div[1]//div[2]//span[1]/text()")
                            prec12 = txtHtml.xpath("//div[@class='columns-container']//li[12]//div[1]//div[2]//span[1]/text()")
                            
                            precios = prec1 + prec2 + prec3 + prec4 + prec5 + prec6 + prec7 + prec8 + prec9 + prec10 + prec11 + prec12

                            for n,p in zip(nombres,precios):
                                print(n +":"+p)
                            return 0
                        except:
                            print("La request tiene una pagina y fallo en esta sección")
                            return -1

                    else:
                        pagina = 1
                        for pagina in range(50):
                            pagina= pagina + 1
                            print(pagina)
                            url2 = "https://www.drogueriascafam.com.co/buscar?search_query=" + medicamento + "&controller=search&orderby=position&orderway=desc&p=" + str(pagina)
                            pagina2 = s.get(url2,proxies={"http": proxy},headers=headers, timeout=5)
                            print(url2, proxies, headers)
                            #print(url2)
                            txtHtml2 = html.fromstring(pagina2.content)
                            sinResultados2 = txtHtml2.xpath("//p[@class='alert alert-warning']/text()")
                            #print(sinResultados)

                            if sinResultados2 ==[]:
                                try:
                                    nombres = txtHtml2.xpath("//span[@class='grid-name']/text()")
                    
                                    prec1 = txtHtml2.xpath("//div[@class='columns-container']//li[1]//div[1]//div[2]//span[1]/text()")
                                    prec2 = txtHtml2.xpath("//div[@class='columns-container']//li[2]//div[1]//div[2]//span[1]/text()")
                                    prec3 = txtHtml2.xpath("//div[@class='columns-container']//li[3]//div[1]//div[2]//span[1]/text()")
                                    prec4 = txtHtml2.xpath("//div[@class='columns-container']//li[4]//div[1]//div[2]//span[1]/text()")
                                    prec5 = txtHtml2.xpath("//div[@class='columns-container']//li[5]//div[1]//div[2]//span[1]/text()")
                                    prec6 = txtHtml2.xpath("//div[@class='columns-container']//li[6]//div[1]//div[2]//span[1]/text()")
                                    prec7 = txtHtml2.xpath("//div[@class='columns-container']//li[7]//div[1]//div[2]//span[1]/text()")
                                    prec8 = txtHtml2.xpath("//div[@class='columns-container']//li[8]//div[1]//div[2]//span[1]/text()")
                                    prec9 = txtHtml2.xpath("//div[@class='columns-container']//li[9]//div[1]//div[2]//span[1]/text()")
                                    prec10 = txtHtml2.xpath("//div[@class='columns-container']//li[10]//div[1]//div[2]//span[1]/text()")
                                    prec11 = txtHtml2.xpath("//div[@class='columns-container']//li[11]//div[1]//div[2]//span[1]/text()")
                                    prec12 = txtHtml2.xpath("//div[@class='columns-container']//li[12]//div[1]//div[2]//span[1]/text()")
                                    
                                    precios = prec1 + prec2 + prec3 + prec4 + prec5 + prec6 + prec7 + prec8 + prec9 + prec10 + prec11 + prec12

                                    for n,p in zip(nombres,precios):
                                        print(n +":"+p)
                                except:
                                    print("La request tiene bastantes productos y fallo en esta sección")
                                    return -2
                    
                            else:
                                break
                else:
                    #break
                    print(sinResultados)
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
