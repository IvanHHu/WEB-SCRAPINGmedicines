import requests as s
import sys
from lxml import html

def main(medicamento):

    #params = {'q': 'CODEINA COMBINACIONES EXCL. SICOLEPTICOS'}
    #q = "losartan"
    url = 'https://www.cruzverde.com.co/search?q=' + medicamento + "&search-button=&lang=es_CO"
    pagina = s.get(url, timeout=5)
    #print(url)
    if pagina.status_code == 200:
        #print("entre")
        pagina.encoding = 'ISO-8859-1'
        txtHtml = html.fromstring(pagina.content)
        urlPAGS = txtHtml.xpath("//span[@class='text-uppercase pagination-text']/text()")
        print(urlPAGS)
        if urlPAGS != [] :
            #print("hola desde paginas")
            url2 = 'https://www.cruzverde.com.co/search?q=' + medicamento + "&search-button=&lang=es_CO&start=12&sz=12"
            pagina2 = s.get(url2, timeout=5)
            txtHtml2 = html.fromstring(pagina2.content)
            print(url2)
            if pagina.status_code == 200:
                print("entre a la pagina 2")
                nombres = txtHtml2.xpath("//a[@class='link']/text()")
                precios = txtHtml2.xpath("//span[@class='value pr-2']/text()")
                for n,p in zip(nombres,precios):
                    n= n.replace("\n        \n            ", "")
                    n= n.replace("\n        \n    ", "")
                    p= p.replace("\n                    ", "")
                    p= p.replace("\n                ", "")
                    print(n +":"+p)

        else:

            nombres = txtHtml.xpath("//a[@class='link']/text()")
            precios = txtHtml.xpath("//span[@class='value pr-2']/text()")
        
            for n,p in zip(nombres,precios):
                n= n.replace("\n        \n            ", "")
                n= n.replace("\n        \n    ", "")
                p= p.replace("\n                    ", "")
                p= p.replace("\n                ", "")
                print(n +":"+p)

        
    else:
        print("Error al cargar la pagina")
            
            

if __name__ == '__main__':
   main(sys.argv[1])
