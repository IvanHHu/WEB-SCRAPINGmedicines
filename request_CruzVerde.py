import requests as s
import sys
from lxml import html

def main(medicamento):
    url = 'https://www.cruzverde.com.co/search?q=' + medicamento + "&search-button=&lang=es_CO"
    pagina = s.get(url, timeout=5)
    #print(url)
    if pagina.status_code == 200:
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
                for pagina in range(50):
                    print(pagina + 1)
                    pagina= pagina*12  
                    url2 = 'https://www.cruzverde.com.co/search?q=' + medicamento + "&search-button=&lang=es_CO&start=" + str(pagina) +"&sz=12"
                    #print(url2)
                    pagina2 = s.get(url2, timeout=5)
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


        
    else:
        print("Error al cargar la pagina")
            
            

if __name__ == '__main__':
   main(sys.argv[1])

