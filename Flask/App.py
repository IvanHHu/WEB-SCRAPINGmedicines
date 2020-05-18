from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS
#---------------------------------------------------------------------------------------------
import requests as s
import bs4
import sys
from lxml import html
from lxml.html import fromstring
from itertools import cycle
import traceback
import random
import json
import wikipedia

app = Flask(__name__)

#My sql connection
app.config[ 'MYSQL_HOST'] = 'localhost'
app.config[ 'MYSQL_USER'] = 'root'
app.config[ 'MYSQL_PASSWORD'] = ''
app.config[ 'MYSQL_DB'] = 'bdmedicines'
mysql = MySQL(app)

CORS(app)
#Settings
#app.secret_key='mysecretkey'

@app.route('/cafam/<medicamento>', methods= ['GET'])
def cafam(medicamento):
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

    result = []
    url = "https://www.drogueriascafam.com.co/buscar?search_query=" + medicamento + "&controller=search&orderby=position&orderway=desc"
    try:
        pagina = s.get(url,proxies={"http": proxy},headers=headers, timeout=5)
        #print(url, proxies, headers)
        if pagina.status_code == 200:
            try:
                pagina.encoding = 'ISO-8859-1'
                txtHtml = html.fromstring(pagina.content)
                sinResultados = txtHtml.xpath("//p[@class='alert alert-warning']/text()")

                if sinResultados ==[]:

                    indPag = txtHtml.xpath("//div[@class='clearfix selector1']/span[1]/text()")
                    #print (indPag)
                    if indPag == []:
                        try:
                            jsonList = []
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
                            
                            for i in range(0,len(nombres)):
                                jsonList.append([{"medicamento" : nombres[i], "precio" : precios[i]}])
                            
                            #result.append(jsonList)
                            return json.dumps(jsonList , indent = 1)
                            return 0
                        except:
                            print("La request tiene una pagina y fallo en esta sección")
                            return -1

                    else:
                        pagina = 1
                        for pagina in range(50):
                            pagina= pagina + 1
                            #print(pagina)
                            url2 = "https://www.drogueriascafam.com.co/buscar?search_query=" + medicamento + "&controller=search&orderby=position&orderway=desc&p=" + str(pagina)
                            pagina2 = s.get(url2,proxies={"http": proxy},headers=headers, timeout=5)
                            #print(url2, proxies, headers)
                            txtHtml2 = html.fromstring(pagina2.content)
                            sinResultados2 = txtHtml2.xpath("//p[@class='alert alert-warning']/text()")
                            #print(sinResultados)

                            if sinResultados2 ==[]:
                                try:
                                    jsonList = []
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
                                    
                                    for i in range(0,len(nombres)):
                                        jsonList.append({"medicamento" : nombres[i], "precio" : precios[i]})
                                    
                                    result.append(jsonList)
                                    
                                except:
                                    print("La request tiene bastantes productos y fallo en esta sección")
                                    return -2
                    
                            else:
                                return json.dumps(result , indent = 1)
                                break
                else:
                    #break
                    print(sinResultados)
                    jsonList = []
                    jsonList.append({"medicamento" : "Sin Resultados", "precio" : "N/A" })
                    result.append(jsonList)
                    return json.dumps(result , indent = 1)
                   
            except:
                    print("La petición hecha no fue exitosa")
                    return 3
        else:
            print("Error al cargar la pagina") 
            return 2   

    except:
        print("Error desconocido al iniciar la petición")
        return 1


@app.route('/cruzverde/<medicamento>', methods= ['GET'])
def cruzverde(medicamento):
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
    result = []
    #------------------------------------------------------------------------------------------------------
    url = 'https://www.cruzverde.com.co/search?q=' + medicamento + "&search-button=&lang=es_CO"
    
    try:
        pagina = s.get(url, proxies={"http": proxy},headers=headers, timeout=5)
        #print(url, proxies, headers)
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
                                pagina= pagina*12  
                                url2 = 'https://www.cruzverde.com.co/search?q=' + medicamento + "&search-button=&lang=es_CO&start=" + str(pagina) +"&sz=12"
                                pagina2 = s.get(url2, proxies={"http": proxy },headers=headers, timeout=5)
 
                                txtHtml2 = html.fromstring(pagina2.content)
                                sinResultados2 = txtHtml2.xpath("//p[@class='no-results-message text-center']/text()")

                                if sinResultados2 == []:
                                    jsonList = []
                                    nombres1 = []
                                    precios1 = []
                                    nombres = txtHtml2.xpath("//a[@class='link']/text()")
                                    precios = txtHtml2.xpath("//span[@class='value pr-2']/text()")

                                    for i in range(0,len(nombres)):
                                        nombres[i] = nombres[i].replace("\n        \n            ", "")
                                        nombres[i] = nombres[i].replace("\n        \n    ", "")
                                        nombres1.append(nombres[i])
                                    
                                    for i in range(0,len(precios)):
                                        precios[i] = precios[i].replace("\n                    ", "")
                                        precios[i] = precios[i].replace("\n                ", "")
                                        precios1.append(precios[i])
                                    #print(nombres1)

                                    for i in range(0,len(precios)):
                                        jsonList.append({"medicamento" : nombres[i], "precio" : precios[i]})

                                    result.append(jsonList)
  
                                else :
                                    return json.dumps(result, indent = 1)
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
                                nombres1.append(nombres[i])
                            
                            for i in range(0,len(precios)):
                                precios[i] = precios[i].replace("\n                    ", "")
                                precios[i] = precios[i].replace("\n                ", "")
                                precios1.append(precios[i])

                            for i in range(0,len(precios)):
                                jsonList.append([{"medicamento" : nombres[i], "precio" : precios[i]}])
                                    
                            return json.dumps(jsonList, indent = 1)
                           
                            #return 0
                        except:
                            print("La request tiene tiene entre 2 y 12 productos y fallo en esta sección")
                            #return -2
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
                                nombres1.append(nombres[i])
                            
                            for i in range(0,len(precios)):
                                precios[i] = precios[i].replace("\n                    ", "")
                                precios[i] = precios[i].replace("\n                ", "")
                               
                                precios1.append(precios[i])
                            
                            for i in range(0,len(precios)):
                                jsonList.append([{"medicamento" : nombres[i], "precio" : precios[i]}])
                                    
                            return json.dumps(jsonList, indent = 1)

                        except:
                            print("La request tiene un producto y fallo en esta sección")
                            #return -1
                else:
                    print(sinResultados[0])
                    jsonList = []
                    jsonList.append({"medicamento" : sinResultados[0], "precio" : "N/A" })
                    result.append(jsonList)
                    return json.dumps(result , indent = 1)
            
            except:
                print("La petición hecha no fue exitosa")
                #return 3
                          
        else:
            print("El request fue exitoso, mas algo paso en la pagina")
            #return 2


    except:
        print("Error desconocido al iniciar la petición")
        #return 1


@app.route('/locatel/<medicamento>', methods = ['GET'])
def locatel(medicamento):
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

    result = []
    #----------------------------------------------------------------------------------------------------------
    proxies = get_proxies()
    proxy_pool = cycle(proxies)
    proxy = next(proxy_pool)

    pag = 0
    for pagina in range(50):
        pag= pag + 1 
        url = "https://www.locatelcolombia.com/buscapagina?ft=" + medicamento + "&PS=12&sl=e3672a70-87b5-474e-b217-cea662d2e462&cc=1&sm=0&PageNumber="+ str(pag)
        #print(pag)
        try:
            pagina = s.get(url, proxies={"http": proxy},headers=headers, timeout=5)
            #print(url, proxies,headers)
            if pagina.status_code == 200:
                try:
                    pagina.encoding = 'ISO-8859-1'
                    jsonList = []
                    if str(pagina.content) != "b''":
                        try:
                            txtHtml = html.fromstring(pagina.content)
                            sinResultados = txtHtml.xpath("//div[@class='page-title']//h2/text()")
                            #print(sinResultados)
                            if sinResultados == []:
                                
                                precios1 = []
                                nombres = txtHtml.xpath("//a[@class='product-name']/text()")
                                precios = txtHtml.xpath("//span[@class='bestPrice']/text()")
                                
                                for i in range(0,len(precios)):
                                    precios[i] = precios[i].replace("\n                ", "")
                                    precios[i] = precios[i].replace("\n            ", "")
                                    precios1.append(precios[i])

                                for i in range(0,len(precios)):
                                    jsonList.append({"medicamento" : nombres[i], "precio" : precios[i]})

                                result.append(jsonList)
                            else:
                                print(sinResultados[0] + "... No hay esultados")
                                
                                return json.dumps(result , indent = 1)
                                #return 0
                        except:
                            print("La request tiene bastantes productos y fallo en esta sección")
                            return -3

                    elif str(pagina.content) == "b''":
                        print(result)
                        if result == []:
                            jsonList.append({"medicamento" : "Sin resultados en Locatel", "precio" : "N/A" })
                            result.append(jsonList)
                            return json.dumps(result, indent = 1)
                            
                        return json.dumps(result, indent = 1)
                        
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

@app.route('/wiki/<medicamento>', methods = ['GET'])
def wiki(medicamento):
    
    wikipedia.set_lang("es")
    parrafo=   wikipedia.summary( medicamento, sentences=2)
    return jsonify({
        'descripcion': parrafo
    })

@app.route('/get_medicines', methods = ['GET'])
def getmedicines():
    medicines = []
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM medicines')
    data = cur.fetchall()
    for medicine in data:
        medicines.append({
            'id': medicine[0],
            'producto': medicine[1],
            'generico': medicine[17]
        })
    return jsonify(medicines)

@app.route('/get_medicine/<medicamento>', methods = ['GET'])
def getmedicine(medicamento):
    medicines = []
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM medicines WHERE producto LIKE'+ '"' + medicamento +'%"')
    data = cur.fetchall()
    print(data)
    if data != ():
        for medicine in data:
            medicines.append({
                'id': medicine[0],
                'producto': medicine[1],
                'generico': medicine[17]
            })
        return jsonify(medicines)
    elif data == ():
        medicines.append({
            'id': "N/A",
            'producto': "No contamos con el medicamento en nuestros datos. Puede buscar directamente el medicamento en la seccion Search",
            'generico': "N/A"
        })
        return jsonify(medicines)



    



if __name__ == '__main__':
    app.run(port = 5000, debug = True)