import requests as s
from bs4 import BeautifulSoup
import sys
from lxml import html

def main(medicamento):
    params = {'producto': 'vayaplin', 'departamento':'Todos'}
    url = "https://www.farmatodo.com.co/"
    print(url)
    pagina = s.get(url, timeout=5)
    #print(url)
    if pagina.status_code == 200:
        print("entre ")
        pagina.encoding = 'ISO-8859-1'
        txtHtml = html.fromstring(pagina.content)
        #print(pagina.content)
        sinResultados = txtHtml.xpath("//span[@class='text-name-user']/b[1]/text()")
        print(sinResultados)

        
        

        
    else:
        print("Error al cargar la pagina")
            
            

if __name__ == '__main__':
   main(sys.argv[1])