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
from operator import itemgetter, attrgetter
from difflib import SequenceMatcher as SM
from collections import Counter

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
        try:
            for i in parser.xpath('//tbody/tr')[:10]:
                if i.xpath('.//td[7][contains(text(),"yes")]'):
                    proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                    proxies.add(proxy)
            return proxies
        except:
            print("Error. Posible proxie bloqueado")
       
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
    try:
        proxies = get_proxies()
        proxy_pool = cycle(proxies)
        proxy = next(proxy_pool)
    except:
        print("Error. Posible proxie bloqueado")

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
                    #print (indPag)// cuando solo hay una pagina
                    if indPag == []:
                        try:
                            jsonList = []
                            nombres = txtHtml.xpath("//span[@class='grid-name']/text()")
                    
                            prec1 = txtHtml.xpath("//div[@class='columns-container']//li[1]//div[1]//div[2]//span[1]/text()")
                            if prec1 != []:
                                prec1[0] = prec1[0].replace(" $ ", "")
                                prec1[0] = prec1[0].replace(" ", "")
                                prec1[0] = prec1[0].replace(",", "")
                                prec1[0] = int(prec1[0])    
                            prec2 = txtHtml.xpath("//div[@class='columns-container']//li[2]//div[1]//div[2]//span[1]/text()")
                            if prec2 != []:
                                prec2[0] = prec2[0].replace(" $ ", "")
                                prec2[0] = prec2[0].replace(" ", "")
                                prec2[0] = prec2[0].replace(",", "")
                                prec2[0] = int(prec2[0])    
                            prec3 = txtHtml.xpath("//div[@class='columns-container']//li[3]//div[1]//div[2]//span[1]/text()")
                            if prec3 != []:
                                prec3[0] = prec3[0].replace(" $ ", "")
                                prec3[0] = prec3[0].replace(" ", "")
                                prec3[0] = prec3[0].replace(",", "")
                                prec3[0] = int(prec3[0])    
                            prec4 = txtHtml.xpath("//div[@class='columns-container']//li[4]//div[1]//div[2]//span[1]/text()")
                            if prec4 != []:
                                prec4[0] = prec4[0].replace(" $ ", "")
                                prec4[0] = prec4[0].replace(" ", "")
                                prec4[0] = prec4[0].replace(",", "")
                                prec4[0] = int(prec4[0])    
                            prec5 = txtHtml.xpath("//div[@class='columns-container']//li[5]//div[1]//div[2]//span[1]/text()")
                            if prec5 != []:
                                prec5[0] = prec5[0].replace(" $ ", "")
                                prec5[0] = prec5[0].replace(" ", "")
                                prec5[0] = prec5[0].replace(",", "")
                                prec5[0] = int(prec5[0])    
                            prec6 = txtHtml.xpath("//div[@class='columns-container']//li[6]//div[1]//div[2]//span[1]/text()")
                            if prec6 != []:
                                prec6[0] = prec6[0].replace(" $ ", "")
                                prec6[0] = prec6[0].replace(" ", "")
                                prec6[0] = prec6[0].replace(",", "")
                                prec6[0] = int(prec6[0])    
                            prec7 = txtHtml.xpath("//div[@class='columns-container']//li[7]//div[1]//div[2]//span[1]/text()")
                            if prec7 != []:
                                prec7[0] = prec7[0].replace(" $ ", "")
                                prec7[0] = prec7[0].replace(" ", "")
                                prec7[0] = prec7[0].replace(",", "")
                                prec7[0] = int(prec7[0])    
                            prec8 = txtHtml.xpath("//div[@class='columns-container']//li[8]//div[1]//div[2]//span[1]/text()")
                            if prec8 != []:
                                prec8[0] = prec8[0].replace(" $ ", "")
                                prec8[0] = prec8[0].replace(" ", "")
                                prec8[0] = prec8[0].replace(",", "")
                                prec8[0] = int(prec8[0])    
                            prec9 = txtHtml.xpath("//div[@class='columns-container']//li[9]//div[1]//div[2]//span[1]/text()")
                            if prec9 != []:
                                prec9[0] = prec9[0].replace(" $ ", "")
                                prec9[0] = prec9[0].replace(" ", "")
                                prec9[0] = prec9[0].replace(",", "")
                                prec9[0] = int(prec9[0])    
                            prec10 = txtHtml.xpath("//div[@class='columns-container']//li[10]//div[1]//div[2]//span[1]/text()")
                            if prec10 != []:
                                prec10[0] = prec10[0].replace(" $ ", "")
                                prec10[0] = prec10[0].replace(" ", "")
                                prec10[0] = prec10[0].replace(",", "")
                                prec10[0] = int(prec10[0])    
                            prec11 = txtHtml.xpath("//div[@class='columns-container']//li[11]//div[1]//div[2]//span[1]/text()")
                            if prec11 != []:
                                prec11[0] = prec11[0].replace(" $ ", "")
                                prec11[0] = prec11[0].replace(" ", "")
                                prec11[0] = prec11[0].replace(",", "")
                                prec11[0] = int(prec11[0])    
                            prec12 = txtHtml.xpath("//div[@class='columns-container']//li[12]//div[1]//div[2]//span[1]/text()")
                            if prec12 != []:
                                prec12[0] = prec12[0].replace(" $ ", "")
                                prec12[0] = prec12[0].replace(" ", "")
                                prec12[0] = prec12[0].replace(",", "")
                                prec12[0] = int(prec12[0])    
                    
                            precios = prec1 + prec2 + prec3 + prec4 + prec5 + prec6 + prec7 + prec8 + prec9 + prec10 + prec11 + prec12
                            caracteres = Counter(medicamento)

                            for i in range(0,len(nombres)):
                                if caracteres[' '] > 1:
                                    coincidencia = SM(None, medicamento, nombres[i]).ratio()
                                    if coincidencia >= 0.1:
                                        print(coincidencia)
                                        jsonList.append({"medicamento" : nombres[i], "precio" : precios[i], "url": url })
                                else:

                                    jsonList.append({"medicamento" : nombres[i], "precio" : precios[i], "url": url })
                            
                            
                            newjson = []
                            print(jsonList)

                            if len(jsonList) == 1:
                                #newjson.append(jsonList)
                                return json.dumps(jsonList , indent = 1)
                           

                            sorted_obj = sorted(jsonList, key=lambda x : x['precio'], reverse=False)

                            return json.dumps(sorted_obj , indent = 1)

                            return 0
                        except:
                            print("La request tiene una pagina y fallo en esta sección")
                            jsonList = []
                            jsonList.append({"medicamento" : "La petición hecha no fue exitosa", "precio" : "N/A",  "url" : url } )
                            #result.append(jsonList)
                            return json.dumps(jsonList , indent = 1)
                            
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
                                    if prec1 != []:
                                        prec1[0] = prec1[0].replace(" $ ", "")
                                        prec1[0] = prec1[0].replace(" ", "")
                                        prec1[0] = prec1[0].replace(",", "")
                                        prec1[0] = int(prec1[0])    
                                    #print (type(prec1[0]))
                                    prec2 = txtHtml2.xpath("//div[@class='columns-container']//li[2]//div[1]//div[2]//span[1]/text()")
                                    if prec2 != []:
                                        prec2[0] = prec2[0].replace(" $ ", "")
                                        prec2[0] = prec2[0].replace(" ", "")
                                        prec2[0] = prec2[0].replace(",", "")
                                        prec2[0] = int(prec2[0])  
                                    prec3 = txtHtml2.xpath("//div[@class='columns-container']//li[3]//div[1]//div[2]//span[1]/text()")
                                    if prec3 != []:
                                        prec3[0] = prec3[0].replace(" $ ", "")
                                        prec3[0] = prec3[0].replace(" ", "")
                                        prec3[0] = prec3[0].replace(",", "")
                                        prec3[0] = int(prec3[0])  
                                    prec4 = txtHtml2.xpath("//div[@class='columns-container']//li[4]//div[1]//div[2]//span[1]/text()")
                                    if prec4 != []:
                                        prec4[0] = prec4[0].replace(" $ ", "")
                                        prec4[0] = prec4[0].replace(" ", "")
                                        prec4[0] = prec4[0].replace(",", "")
                                        prec4[0] = int(prec4[0])  
                                   
                                    prec5 = txtHtml2.xpath("//div[@class='columns-container']//li[5]//div[1]//div[2]//span[1]/text()")
                                    if prec5 != []:
                                        prec5[0] = prec5[0].replace(" $ ", "")
                                        prec5[0] = prec5[0].replace(" ", "")
                                        prec5[0] = prec5[0].replace(",", "")
                                        prec5[0] = int(prec5[0])  

                                    prec6 = txtHtml2.xpath("//div[@class='columns-container']//li[6]//div[1]//div[2]//span[1]/text()")
                                    if prec6 != []:
                                        prec6[0] = prec6[0].replace(" $ ", "")
                                        prec6[0] = prec6[0].replace(" ", "")
                                        prec6[0] = prec6[0].replace(",", "")
                                        prec6[0] = int(prec6[0])  

                                    prec7 = txtHtml2.xpath("//div[@class='columns-container']//li[7]//div[1]//div[2]//span[1]/text()")
                                    if prec7 != []:
                                        prec7[0] = prec7[0].replace(" $ ", "")
                                        prec7[0] = prec7[0].replace(" ", "")
                                        prec7[0] = prec7[0].replace(",", "")
                                        prec7[0] = int(prec7[0])  

                                    prec8 = txtHtml2.xpath("//div[@class='columns-container']//li[8]//div[1]//div[2]//span[1]/text()")
                                    if prec8 != []:
                                        prec8[0] = prec8[0].replace(" $ ", "")
                                        prec8[0] = prec8[0].replace(" ", "")
                                        prec8[0] = prec8[0].replace(",", "")
                                        prec8[0] = int(prec8[0])  

                                    prec9 = txtHtml2.xpath("//div[@class='columns-container']//li[9]//div[1]//div[2]//span[1]/text()")
                                    if prec9 != []:
                                        prec9[0] = prec9[0].replace(" $ ", "")
                                        prec9[0] = prec9[0].replace(" ", "")
                                        prec9[0] = prec9[0].replace(",", "")
                                        prec9[0] = int(prec9[0])  

                                    prec10 = txtHtml2.xpath("//div[@class='columns-container']//li[10]//div[1]//div[2]//span[1]/text()")
                                    if prec10 != []:
                                        prec10[0] = prec10[0].replace(" $ ", "")
                                        prec10[0] = prec10[0].replace(" ", "")
                                        prec10[0] = prec10[0].replace(",", "")
                                        prec10[0] = int(prec10[0])  

                                    prec11 = txtHtml2.xpath("//div[@class='columns-container']//li[11]//div[1]//div[2]//span[1]/text()")
                                    if prec11 != []:
                                        prec11[0] = prec11[0].replace(" $ ", "")
                                        prec11[0] = prec11[0].replace(" ", "")
                                        prec11[0] = prec11[0].replace(",", "")
                                        prec11[0] = int(prec11[0])  
                                    prec12 = txtHtml2.xpath("//div[@class='columns-container']//li[12]//div[1]//div[2]//span[1]/text()")
                                    if prec12 != []:
                                        prec12[0] = prec12[0].replace(" $ ", "")
                                        prec12[0] = prec12[0].replace(" ", "")
                                        prec12[0] = prec12[0].replace(",", "")
                                        prec12[0] = int(prec12[0])  
                                    
                                    
                                    precios = prec1 + prec2 + prec3 + prec4 + prec5 + prec6 + prec7 + prec8 + prec9 + prec10 + prec11 + prec12
                                    #print(precios)
                                    caracteres = Counter(medicamento)
                                    #print(caracteres[' '])
                                    for i in range(0,len(nombres)):
                                        if caracteres[' '] == 0:
                                            jsonList.append({"medicamento" : nombres[i], "precio" : precios[i],  "url" : url2 })
                                        else:
                                            coincidencia = SM(None, medicamento, nombres[i]).ratio()
                                            #print(coincidencia)
                                            if coincidencia >= 0.2:
                                                jsonList.append({"medicamento" : nombres[i], "precio" : precios[i],  "url" : url2 })

                                    result.append(jsonList)
                                    #print(jsonList)
                                    
                                    
                                except:
                                    print("La request tiene bastantes productos y fallo en esta sección")
                                    jsonList == []
                                    jsonList.append({"medicamento" : "La petición hecha no fue exitosa, posible error en una pagina de productos", "precio" : "N/A",   "url" : "N/A" })
                                    #result.append(jsonList)
                                    return json.dumps(jsonList , indent = 1)
                                    return -2
                    
                            else:
                                #orden de precios
                                if jsonList == []:
                                    print("Hubo resultados pero no coincidencias")
                                    result = []
                                    jsonList.append({"medicamento" : "Hay resultados en la pagina, pero ninguno coincide", "precio" : "N/A",  "url" : "N/A" })
                                    result.append(jsonList)
                                    return json.dumps(result , indent = 1)

                                else:
                                    newjson = []
                                    for i in range(1,len(result)):
                                        if newjson == []:
                                            newjson = result[0] + result[i ]
                                        else:
                                            newjson = newjson + result[i]
                                            if i == len(result):
                                                newjson.append(newjson)
                                    
                                    sorted_obj = sorted(newjson, key=lambda x : x['precio'], reverse=False)
                                    return json.dumps(sorted_obj , indent = 1)

                                break
                else:
                    #break
                    #print(sinResultados)
                    jsonList = []
                    jsonList.append({"medicamento" : "Sin Resultados", "precio" : "N/A",  "url" : "N/A" })
                    #result.append(jsonList)
                    return json.dumps(jsonList , indent = 1)
                   
            except:
                    print("La petición hecha no fue exitosa")
                    jsonList = []
                    jsonList.append({"medicamento" : "La petición hecha no fue exitosa", "precio" : "N/A" })
                    #result.append(jsonList)
                    return json.dumps(jsonList , indent = 1)
                    return 3
        else:
            print("Error al cargar la pagina") 
            return 2   

    except:
        print("Error desconocido al iniciar la petición")
        jsonList = []
        jsonList.append({"medicamento" : "La pagina no cargo correctamente, tiene problemas tecnicos o hay un proxie bloqueado. Intentelo mas tarde.", "precio" : "N/A",  "url" : "N/A" })
        #result.append(jsonList)
        return json.dumps(jsonList , indent = 1)
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
    try:
        proxies = get_proxies()
        proxy_pool = cycle(proxies)
        proxy = next(proxy_pool)
    except:
        print("Error. Proxie bloqueado")


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
                                    precios2 = []
                                    nombres = txtHtml2.xpath("//a[@class='link']/text()")
                                    for i in range(0,len(nombres)):
                                        nombres[i] = nombres[i].replace("\n        \n            ", "")
                                        nombres[i] = nombres[i].replace("\n        \n    ", "")
                                        nombres1.append(nombres[i])

                                    precios = txtHtml2.xpath("//span[@class='value pr-2']/text()")
                                    #print(precios)
                                    if precios != []:
                                        #print(precios)
                                        for i in range(0,len(precios)):
                                            precios[i] = precios[i].replace("\n                    ", "")
                                            precios[i] = precios[i].replace("\n                ", "")
                                            precios[i] = precios[i].replace("$", "")
                                            precios[i] = precios[i].replace(".", "")
                                            precios2.append(precios[i])


                                    preciosOferta = txtHtml2.xpath("//span[@class='value']/text()")
                                    #print(preciosOferta)
                                    preciosOferta2= []
                                    if preciosOferta != []:        
                                        #print(preciosOferta)
                                        for i in range(0,len(preciosOferta)):
                                            preciosOferta[i] = preciosOferta[i].replace("\n                \n                \n                    ", "")
                                            preciosOferta[i] = preciosOferta[i].replace("\n\n\n                    \n                        (Oferta)\n                    \n                \n                ", "" )
                                            preciosOferta[i] = preciosOferta[i].replace("\n                    ", "")
                                            preciosOferta[i] = preciosOferta[i].replace("\n\n                    \n                    ", "")
                                            preciosOferta[i] = preciosOferta[i].replace("\n                ", "")
                                            preciosOferta[i] = preciosOferta[i].replace("\n                    ", "")
                                            preciosOferta[i] = preciosOferta[i].replace("\n                ", "")
                                            preciosOferta[i] = preciosOferta[i].replace("\n", "")
                                            preciosOferta[i] = preciosOferta[i].replace("$", "")
                                            preciosOferta[i] = preciosOferta[i].replace(".", "")
                                            preciosOferta[i] = preciosOferta[i].replace("                                    ", "")
                                            
                                            if preciosOferta[i] != '':
                                                preciosOferta2.append(preciosOferta[i])

                                    preciosFull = precios2 + preciosOferta2

                                    for i in range(0,len(preciosFull)):
                                       preciosFull[i] = float(preciosFull[i])
                                    
                                    caracteres = Counter(medicamento)

                                    for i in range(0,len(preciosFull)):
                                        if caracteres[' '] > 1:
                                            coincidencia = SM(None, medicamento, nombres[i]).ratio()
                                            #print(coincidencia)
                                            if coincidencia >= 0.1:
                                                jsonList.append({"medicamento" : nombres[i], "precio" : preciosFull[i], "url": url2})

                                        else:
                                            jsonList.append({"medicamento" : nombres[i], "precio" : preciosFull[i], "url": url2})

                                    result.append(jsonList)
  
                                else :

                                    if jsonList == []:
                                        jsonList.append({"medicamento" : "Sin resultados", "precio" : "N/A", "url":"N/A" })
                                        return json.dumps(jsonList, indent = 1)

                                    #print(result)
                                    newjson = []
                                    for i in range(1,len(result)):
                                        if newjson == []:
                                            newjson = result[0] + result[i ]
                                        else:
                                            newjson = newjson + result[i]
                                            if i == len(result):
                                                newjson.append(newjson)

                                    sorted_obj = sorted(newjson, key=lambda x : x['precio'], reverse=False)

                                    return json.dumps(sorted_obj, indent = 1)
                                    break
                            return 0
                        except:
                            print("La request tiene bastantes productos y fallo en esta sección")
                            jsonList = []
                            #result = []
                            jsonList.append({"medicamento" : "La petición hecha no fue exitosa", "precio" : "N/A", "url": "N/A" })
                            #result.append(jsonList)
                            return json.dumps(jsonList , indent = 1)

                            return -3
                    #cuando solo hay un medicamento
                    elif fichaTec != []:
                        try:
                            jsonList = []
                            nombres1 = []
                            precios2 = []
                            nombres = txtHtml.xpath("//h1[@class='product-name']/text()")
                            for i in range(0,len(nombres)):
                                nombres[i] = nombres[i].replace("\n        \n            ", "")
                                nombres[i] = nombres[i].replace("\n        \n    ", "")
                                nombres1.append(nombres[i])

                            precios = txtHtml.xpath("//span[@class='value pr-2']/text()")
                            if precios != []:
                                for i in range(0,len(precios)):
                                    precios[i] = precios[i].replace("\n                    ", "")
                                    precios[i] = precios[i].replace("\n                ", "")
                                    precios[i] = precios[i].replace("$", "")
                                    precios[i] = precios[i].replace(".", "")
                                    precios2.append(precios[i])

                            preciosOferta = txtHtml.xpath("//span[@class='value']/text()")
                            #print(preciosOferta)
                            preciosOferta2= []
                            if preciosOferta != []:        
                                #print(preciosOferta)
                                for i in range(0,len(preciosOferta)):
                                    preciosOferta[i] = preciosOferta[i].replace("\n                \n                \n                    ", "")
                                    preciosOferta[i] = preciosOferta[i].replace("\n\n\n                    \n                        (Oferta)\n                    \n                \n                ", "" )
                                    preciosOferta[i] = preciosOferta[i].replace("\n                    ", "")
                                    preciosOferta[i] = preciosOferta[i].replace("\n\n                    \n                    ", "")
                                    preciosOferta[i] = preciosOferta[i].replace("\n                ", "")
                                    preciosOferta[i] = preciosOferta[i].replace("\n                    ", "")
                                    preciosOferta[i] = preciosOferta[i].replace("\n                ", "")
                                    preciosOferta[i] = preciosOferta[i].replace("\n", "")
                                    preciosOferta[i] = preciosOferta[i].replace("$", "")
                                    preciosOferta[i] = preciosOferta[i].replace(".", "")
                                    preciosOferta[i] = preciosOferta[i].replace("                                    ", "")
                                    
                                    if preciosOferta[i] != '':
                                        preciosOferta2.append(preciosOferta[i])

                            
                            preciosFull = precios2 + preciosOferta2

                            for i in range(0,len(preciosFull)):
                                preciosFull[i] = float(preciosFull[i])
                        

                            for i in range(0,len(nombres1)-1):
                                jsonList.append([{"medicamento" : nombres1[i], "precio" : preciosFull[i], "url": url }])
                            
                            
                            return json.dumps(jsonList, indent = 1)
                           
                            #return 0
                        except:
                            print("La request tiene un producto y fallo en esta sección")
                            jsonList = []
                            jsonList.append({"medicamento" : "La petición hecha no fue exitosa", "precio" : "N/A", "url":"N/A" })
                            #result.append(jsonList)
                            return json.dumps(jsonList , indent = 1)
                            #return -2
                    #cuando hay solo una pagina
                    elif fichaTec == []:
                        try:
                            jsonList = []
                            nombres1 = []
                            precios2 = []
                            nombres = txtHtml.xpath("//a[@class='link']/text()")
                            for i in range(0,len(nombres)):
                                nombres[i] = nombres[i].replace("\n        \n            ", "")
                                nombres[i] = nombres[i].replace("\n        \n    ", "")
                                nombres1.append(nombres[i])


                            precios = txtHtml.xpath("//span[@class='value pr-2']/text()")
                            for i in range(0,len(precios)):
                                if precios != []:
                                    precios[i] = precios[i].replace("\n                    ", "")
                                    precios[i] = precios[i].replace("\n                ", "")
                                    precios[i] = precios[i].replace("$", "")
                                    precios[i] = precios[i].replace(".", "")
                                    precios2.append(precios[i])
                            

                            preciosOferta = txtHtml.xpath("//span[@class='value']/text()")
                            preciosOferta2= []
                            if preciosOferta != []:        
                                #print(preciosOferta)
                                for i in range(0,len(preciosOferta)):
                                    preciosOferta[i] = preciosOferta[i].replace("\n                \n                \n                    ", "")
                                    preciosOferta[i] = preciosOferta[i].replace("\n\n\n                    \n                        (Oferta)\n                    \n                \n                ", "" )
                                    preciosOferta[i] = preciosOferta[i].replace("\n                    ", "")
                                    preciosOferta[i] = preciosOferta[i].replace("\n\n                    \n                    ", "")
                                    preciosOferta[i] = preciosOferta[i].replace("\n                ", "")
                                    preciosOferta[i] = preciosOferta[i].replace("\n                    ", "")
                                    preciosOferta[i] = preciosOferta[i].replace("\n                ", "")
                                    preciosOferta[i] = preciosOferta[i].replace("\n", "")
                                    preciosOferta[i] = preciosOferta[i].replace("$", "")
                                    preciosOferta[i] = preciosOferta[i].replace(".", "")
                                    preciosOferta[i] = preciosOferta[i].replace("                                    ", "")
                                    
                                    if preciosOferta[i] != '':
                                        preciosOferta2.append(preciosOferta[i])


                            preciosFull = precios2 + preciosOferta2
                            caracteres = Counter(medicamento)
                            #printprint(caracteres)
                            #print(len(preciosFull)-1)

                            for i in range(0,len(preciosFull)):
                                preciosFull[i] = float(preciosFull[i])

                            #print(len(nombres1))
                            for i in range(0,len(nombres1)):
                                if nombres1[i] != []:
                                    if caracteres[' '] == 0:
                                        jsonList.append({"medicamento" : nombres1[i], "precio" : preciosFull[i], "url": url })
                                    else:
                                        coincidencia = SM(None, medicamento, nombres1[i]).ratio()
                                        print(coincidencia)
                                        if coincidencia >= 0.2:
                                            jsonList.append({"medicamento" : nombres1[i], "precio" : preciosFull[i], "url": url })


                            print(jsonList)

                            if jsonList == []:
                                jsonList.append({"medicamento" : "Sin resultados", "precio" : "N/A", "url":"N/A" })
                                return json.dumps(jsonList, indent = 1)


                            else:
                                sorted_obj = sorted(jsonList, key=lambda x : x['precio'], reverse=False)
                                print(sorted_obj)

                                return json.dumps(sorted_obj , indent = 1)


                            #return json.dumps(jsonList, indent = 1)

                        except:
                            print("La request tiene una pagina y fallo en esta sección")
                            jsonList = []
                            jsonList.append({"medicamento" : "La petición hecha no fue exitosa", "precio" : "N/A", "url":"N/A" })
                            #result.append(jsonList)
                            return json.dumps(jsonList , indent = 1)
                            #return -1
                else:
                    #print(sinResultados[0])
                    jsonList = []
                    jsonList.append({"medicamento" : "Sin resultados", "precio" : "N/A", "url":"N/A" })
                    #result.append(jsonList)
                    return json.dumps(jsonList , indent = 1)
            
            except:
                print("La petición hecha no fue exitosa")
                jsonList = []
                jsonList.append({"medicamento" : "La petición hecha no fue exitosa", "precio" : "N/A", "url":"N/A" })
                #result.append(jsonList)
                return json.dumps(jsonList , indent = 1)
                #return 3
                          
        else:
            print("El request fue exitoso, mas algo paso en la pagina")
            #return 2


    except:
        print("Error desconocido al iniciar la petición")
        jsonList = []
        jsonList.append({"medicamento" : "Error desconocido al iniciar la petición", "precio" : "N/A", "url":"N/A" })
        #result.append(jsonList)
        return json.dumps(jsonList , indent = 1)
        #return 1


@app.route('/locatel/<medicamento>', methods = ['GET'])
def locatel(medicamento):
    def get_proxies():
        url = 'https://free-proxy-list.net/'
        response = s.get(url)
        parser = fromstring(response.text)
        proxies = set()
        try:
            for i in parser.xpath('//tbody/tr')[:10]:
                if i.xpath('.//td[7][contains(text(),"yes")]'):
                    proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                    proxies.add(proxy)
            return proxies
        except:
            print("Error. Proxie bloqueado")
    
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
    urlPrueba = "https://www.locatelcolombia.com/" + medicamento
    #----------------------------------------------------------------------------------------------------------
    try:
        proxies = get_proxies()
        proxy_pool = cycle(proxies)
        proxy = next(proxy_pool)
    except:
        print("Posible proxie bloqueado")

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
                                    precios[i] = precios[i].replace("$", "")
                                    precios[i] = precios[i].replace(".", "")
                                    precios[i] = precios[i].replace(",", ".")
                                    precios[i] = float(precios[i])  
                                    precios1.append(precios[i])

                                caracteres = Counter(medicamento)
                                #print(caracteres[' '])

                                for i in range(0,len(precios)):
                                    if caracteres[' '] > 1:
                                        coincidencia = SM(None, medicamento, nombres[i]).ratio()
                                        #print(coincidencia)
                                        if coincidencia >= 0.5:
                                            jsonList.append({"medicamento" : nombres[i], "precio" : precios[i], "url": urlPrueba})

                                    else:
                                        jsonList.append({"medicamento" : nombres[i], "precio" : precios[i], "url": urlPrueba})

                                #print(jsonList)
                                result.append(jsonList)
                            else:
                                print(sinResultados[0] + "... No hay esultados")
                                #print(result)
                                return json.dumps(result , indent = 1)
                                #return 0
                        except:
                            print("La request tiene bastantes productos y fallo en esta sección")
                            jsonList.append({"medicamento" : "La petición hecha no fue exitosa", "precio" : "N/A", "url":"N/A" })
                            #result.append(jsonList)
                            return json.dumps(jsonList, indent = 1)
                            return -3

                    elif str(pagina.content) == "b''":
                        #print(result)
                        #if jsonList == []:
                            #jsonList.append({"medicamento" : "Sin resultados en Locatel", "precio" : "N/A", "url":"N/A" })
                            #return json.dumps(jsonList, indent = 1)
                        #print(result)

                        if result == []:
                            jsonList.append({"medicamento" : "Sin resultados en Locatel", "precio" : "N/A", "url": "N/A" })
                            #result.append(jsonList)
                            return json.dumps(jsonList, indent = 1)
                        
                        if result[0] == []:
                            jsonList =  []
                            jsonList.append({"medicamento" : "Sin resultados en Locatel", "precio" : "N/A", "url": "N/A" })
                            #result.append(jsonList)
                            return json.dumps(jsonList, indent = 1)

                        
                        if len(result) > 1:
                            newjson = []
                            for i in range(1,len(result)):
                                if newjson == []:
                                    newjson = result[0] + result[i]
                                    #print(newjson)
                                else:
                                    newjson = newjson + result[i]
                                    #print(newjson)
                                    if i == len(result):
                                        newjson.append(newjson)
                            
                            sorted_obj = sorted(newjson, key=lambda x : x['precio'], reverse=False)
                            return json.dumps(sorted_obj, indent = 1)

                        else:
                            sorted_obj = sorted(result[0], key=lambda x : x['precio'], reverse=False)
                            return json.dumps(sorted_obj, indent = 1)
                        
                        break
                except:
                    print("La petición hecha no fue exitosa")
                    jsonList.append({"medicamento" : "La petición hecha no fue exitosa", "precio" : "N/A",  "url":"N/A" })
                    #result.append(jsonList)
                    return json.dumps(jsonList, indent = 1)
                    return 1
                    return 3
                
            else:
                print("Error al cargar la pagina")

                return 2
        except:
            print("Error desconocido al iniciar la petición")
            jsonList.append({"medicamento" : "Error desconocido al iniciar la petición", "precio" : "N/A",  "url":"N/A" })
            #result.append(jsonList)
            return json.dumps(jsonList, indent = 1)
            return 1

@app.route('/wiki/<medicamento>', methods = ['GET'])
def wiki(medicamento):
    descripcion= []
    try:
        wikipedia.set_lang("es")
        parrafo = wikipedia.summary( medicamento, sentences=2)

        descripcion.append({
                'medicamento': medicamento,
                'descripcion': parrafo
            })
        return jsonify( descripcion)
        
    except :
        descripcion.append({
                'medicamento': medicamento,
                'descripcion': "Sin resultados en wikipedia"
            })
        return jsonify( descripcion)


@app.route('/get_last_medicines', methods = ['GET'])
def getlastmedicines():
    medicines = []
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM ( SELECT * FROM medicines ORDER BY id DESC LIMIT 50 ) sub ORDER BY id ASC')
    data = cur.fetchall()
    for medicine in data:
        medicines.append({
            'id': medicine[0],
            'producto': medicine[1],
            'generico': medicine[17]
        })
    return jsonify(medicines)


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
    coincidencias = []
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM medicines WHERE producto LIKE'+ '"' + medicamento +'%"')
    data = cur.fetchall()
    #print(data)
    if data != ():
        for medicine in data:
            #print(coincidencias)

            if (coincidencias == []):
                coincidencias.append({
                'id': medicine[0],
                'producto': medicine[1],
                #'desComercial': medicine[10],
                'generico': medicine[17]
                })

            else:
                if any(tag['producto'] == medicine[1] for tag in coincidencias):
                    print("si hay un producto existente")

                else:
                    coincidencias.append({
                    'id': medicine[0],
                    'producto': medicine[1],
                    'generico': medicine[17]
                    })

            
        return jsonify(coincidencias)



    elif data == ():
        coincidencias.append({
            'id': "N/A",
            'producto': "No contamos con el medicamento en nuestros datos. Puede buscar directamente el medicamento en la seccion Search",
            'generico': "N/A"
        })
        return jsonify(coincidencias)

@app.route('/get_medicine2/<medicamento>', methods = ['GET'])
def getmedicine2(medicamento):
    coincidencias = []
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM medicines2 WHERE producto LIKE'+ '"' + medicamento +'%"')
    data = cur.fetchall()
    #print(data)
    if data != ():
        for medicine in data:
            #print(coincidencias)
            if (coincidencias == []):
                coincidencias.append({
                'id': medicine[0],
                'producto': medicine[1],
                'generico': medicine[3]
                })
            else:
                if any(tag['producto'] == medicine[1] for tag in coincidencias):
                    print("si hay un producto existente")
                else:
                    coincidencias.append({
                    'id': medicine[0],
                    'producto': medicine[1],
                    'generico': medicine[3]
                    })
        return jsonify(coincidencias)
    elif data == ():
        coincidencias.append({
            'id': "N/A",
            'producto': "No contamos con el medicamento en nuestros datos. Puede buscar directamente el medicamento en la seccion Search"
        })
        return jsonify(coincidencias)

@app.route('/get_medicine3/<medicamento>', methods = ['GET'])
def getmedicine3(medicamento):
    coincidencias = []
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, presentacion from medicines2 WHERE producto LIKE' '"' + medicamento +'%"')
    data = cur.fetchall()
    #print(data)
    if data != ():
        for medicine in data:
            #print(coincidencias)

            if (coincidencias == []):
                coincidencias.append({
                'id': medicine[0],
                'presentacion': medicine[1]
                #'desComercial': medicine[10],
                })

            else:
                if any(tag['id'] == medicine[0] for tag in coincidencias):
                    print("si hay un producto existente")

                else:
                    coincidencias.append({
                    'id': medicine[0],
                    'presentacion': medicine[1]
                    })

            
        return jsonify(coincidencias)



    elif data == ():
        coincidencias.append({
            'id': "N/A",
            'producto': "No contamos con el medicamento en nuestros datos. Puede buscar directamente el medicamento en la seccion Search",
            'generico': "N/A"
        })
        return jsonify(coincidencias)



if __name__ == '__main__':
    app.run(port = 5000, debug = True)