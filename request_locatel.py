import requests as s
import sys
from lxml import html

def main(medicamento):
    headers = {
        "Referer": "https://www.locatelcolombia.com/buscapagina?ft=vitamina&PS=12&sl=e3672a70-87b5-474e-b217-cea662d2e462&cc=1&sm=0&PageNumber=2",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36",
        "x-requested-with":"XMLHttpRequest"

    }
    


    url = "https://www.locatelcolombia.com/buscapagina?ft=" + medicamento + "&PS=12&sl=e3672a70-87b5-474e-b217-cea662d2e462&cc=1&sm=0&PageNumber=1"
    print(url)
    pagina = s.get(url, timeout=5)
    #print(url)
    if pagina.status_code == 200:
        print("entre ")
        pagina.encoding = 'ISO-8859-1'
        txtHtml = html.fromstring(pagina.content)
        #print(pagina.content)
        sinResultados = txtHtml.xpath("//div[@class='page-title']//h2/text()")
        #print(sinResultados)

        if sinResultados == []:
            #print("si hay :v")
            nombres = txtHtml.xpath("//a[@class='product-name']/text()")
            precios = txtHtml.xpath("//span[@class='bestPrice']/text()")
            for n,p in zip(nombres,precios):
                p= p.replace("\n                ", "")
                p= p.replace("\n            ", "")
                print(n +":"+p)
            #print(nombres)

        else:
            print(sinResultados[0] + "... No hay esultados")

        
        

        
    else:
        print("Error al cargar la pagina")
            
            

if __name__ == '__main__':
   main(sys.argv[1])