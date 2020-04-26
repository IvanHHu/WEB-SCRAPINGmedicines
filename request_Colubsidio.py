import requests as s
import sys
from lxml import html

def main(medicamento):
    url = "https://www.drogueriascolsubsidio.com/" + medicamento 
    print(url)
    pagina = s.get(url, timeout=5)
    #print(url)
    if pagina.status_code == 200:
        #print("entre ")
        pagina.encoding = 'ISO-8859-1'
        txtHtml = html.fromstring(pagina.content)
        sinResultados = txtHtml.xpath("//div[@class='subtitle-error']/text()")

        if sinResultados == []:
            #print("si hay :v")
            nombres = txtHtml.xpath("/html/body/section/section/div[2]/text()")
            
            precios = txtHtml.xpath("//p[@class='dataproducto-bestPrice'][2]/text()")
            print(nombres)
            #print(precios)
            #print(precios)
            
        

        else:
            print(sinResultados[0])
      
        

        
    else:
        print("Error al cargar la pagina")
            
            

if __name__ == '__main__':
   main(sys.argv[1])
