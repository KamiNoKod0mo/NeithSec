import requests, re, os
import xml.etree.ElementTree as ET
from fpdf import FPDF
from pdfrw import PdfReader, PdfWriter, PageMerge


def expliot_db(search):
    # URL da requisição
    url = "https://www.exploit-db.com/?draw=15&columns%5B0%5D%5Bdata%5D=date_published&columns%5B0%5D%5Bname%5D=date_published&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=download&columns%5B1%5D%5Bname%5D=download&columns%5B1%5D%5Bsearchable%5D=false&columns%5B1%5D%5Borderable%5D=false&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=application_md5&columns%5B2%5D%5Bname%5D=application_md5&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=false&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=verified&columns%5B3%5D%5Bname%5D=verified&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=false&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=description&columns%5B4%5D%5Bname%5D=description&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=false&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=type_id&columns%5B5%5D%5Bname%5D=type_id&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=false&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=platform_id&columns%5B6%5D%5Bname%5D=platform_id&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=false&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=author_id&columns%5B7%5D%5Bname%5D=author_id&columns%5B7%5D%5Bsearchable%5D=false&columns%5B7%5D%5Borderable%5D=false&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=code&columns%5B8%5D%5Bname%5D=code.code&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=id&columns%5B9%5D%5Bname%5D=id&columns%5B9%5D%5Bsearchable%5D=false&columns%5B9%5D%5Borderable%5D=true&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=9&order%5B0%5D%5Bdir%5D=desc&start=0&length=15&search%5Bregex%5D=false&author=&port=&type=&tag=&platform=&_=1715179675440"

    # Cabeçalhos da requisição
    headers = {
        "Cookie": "CookieConsent={stamp:%27-1%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27implied%27%2Cver:1%2Cutc:1715128131800%2Cregion:%27BR%27}; _ga=GA1.3.439348186.1715128133; _gid=GA1.3.42379335.1715128133; _gat=1; _ga_N0K6XSDCRJ=GS1.3.1715179678.2.0.1715179678.60.0.0; XSRF-TOKEN=eyJpdiI6IldacVh3XC9sU1pJUk9oek4zdE5ucmpBPT0iLCJ2YWx1ZSI6IkNJaW53R1JnRWZsNnZxVnZxNXZESW9HMWY3RGJNdjhuek1tc1hRNjFGM0RlVlNcL1hndkt3d3FcL1p5OGd4RktXQiIsIm1hYyI6IjVmZTc1ZGZkNjYyZjc1MzU5ODI2NGMzM2YxYTY0NmZmZmViOTZhMmFmYWMwNWQ1NTYzNjA5NDQ4ZWQxNmFlNDgifQ%3D%3D; exploit_database_session=eyJpdiI6IjlicUZhWlZ3blFMS1wvRU5RYURGTmNBPT0iLCJ2YWx1ZSI6IkF4WlR2K1hVVlFhUUFjXC9oRWV1S2R6YlEyejB0RXJYRlNwUG8zR0ZTb3RtR1h1VWFqdkN1UThlNlFoY3p1eVIxIiwibWFjIjoiY2YzMzY4ZjI2YmRhMzA3MDkxMzQ1Y2JhYzFmOTIwZWZjM2Y2NDYwZWY0YzAxNWIwMGRkZmU1ZGYzZTAyNjc5OCJ9",
        "Sec-Ch-Ua": "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36",
        "Sec-Ch-Ua-Platform": "\"Linux\"",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.exploit-db.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Priority": "u=1, i"
    }

    # Enviar a solicitação GET
    dados = 'search%5Bvalue%5D='+ search
    resposta = requests.get(url, headers=headers, params=dados)
    return resposta


infos = []
def output(path,data,vf,vuln_explain):
    global infos
    infos.append([f'{data[0][1]}\n',f'\t{data[1][1]}\n',f'\t {vuln_explain}\n\n'])
    #print(vf)
    if vf == False:
        #print(infos)
        salvar_em_pdf(infos,path)
        infos = []     

def filtrar_hosts_nmap(arquivo):
    resultados = []
    sistema = []
    
    # Analisar o arquivo XML
    tree = ET.parse(arquivo)
    root = tree.getroot()
    
    portas_abertas = []
    servicos = []

    versions = []
    states = []
    products = []
    
    protocols = []
    resut_protocols = []
    
    # Iterar sobre cada host no arquivo
    for host in root.findall('.//host'):
        
        sistema.append({'ip': host.find('.//address').attrib['addr']})
        sistema.append({'so':host.find('.//os/osmatch').attrib['name']})
    
        
    # Iterar sobre cada porta aberta no host
    for porta in host.findall('.//port'):
        numero_porta = porta.attrib['portid']
        protocolo = porta.attrib['protocol']
        portas_abertas.append({'porta': numero_porta, 'protocolo': protocolo})
        #print(numero_porta)
        
    for state in host.findall('.//state'):
        state = state.attrib['state']
        states.append(state)
    
    for servico in host.findall('.//service'):
        try:
            version = servico.attrib['version']
            #print(version)
            versions.append(version)
            
            
        except:
            versions.append('')
        try:
            prod = servico.attrib['product']
            products.append(prod)
        except:
            products.append('')
            
        servico = servico.attrib['name']
        servicos.append(servico)
        
    
    for num in range(len(portas_abertas)):
        portas_abertas[num]['servico']=  servicos[num]
        portas_abertas[num]['version']=  versions[num]
        portas_abertas[num]['state']=  states[num]
        portas_abertas[num]['product']=  products[num]
        #print(versions)
    
    resultados.append(portas_abertas)
    
    resut_protocols.append(sistema)
    

    for protocol in resultados[0]:
        if protocol['state'] == 'open':
            protocols.append(protocol)
            
    resut_protocols.append(protocols)
    #print(resut_protocols)
    return resut_protocols
  

def ai_response(vuln):
    #url + chave API
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=AIzaSyA1EJqNhbt1CXAPIbOCgRxfTcMBduQWImo'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36",
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [{
            "parts": [{
                "text": f"Explique com 1000 palavras o que é {vuln} e como se proteger com comandos em ambientes Linux e Windows"
            }]
        }]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    
    # Sobre a vulnerabilidade
    #print(vuln)
    data = response.json()
    #print(data)
    #response = requests.get(url, headers=headers, json=payload)
    return (data["candidates"][0]["content"]["parts"][0]["text"])
    

#ai_response('Cybrotech CyBroHttpServer 1.0.3 - Cross-Site Scripting')
def salvar_em_pdf(texto, nome_arquivo):
    #padrao = r"\*\*(.*?)\*\*"
    pdf = FPDF()
    pdf.add_page()
    #print(texto)
    #x = 0 
    pdf.set_font("Arial", size=12)
    for i in range(0,len(texto)):
        
        
        pdf.set_font("Arial", style='B', size=16)
        pdf.cell(0, 10, txt=infos[i][0],ln=True, align='C')
        pdf.set_font("Arial", style='B', size=14)
        pdf.cell(0, 10, txt=infos[i][1],ln=True, align='C')
        pdf.set_font("Arial", size=12)
        

        for line in infos[i][2].splitlines():
            #print(line)
            if line.strip():
                if re.search(padrao, line):
                    pdf.ln()
                    pdf.set_font("Arial", style='B', size=12)
                    pdf.multi_cell(0, 10,txt=line.replace('**', '').replace('* ', '- '))
                    #pdf.ln()
                #elif re.search()
                else:
                    pdf.set_font("Arial", style='',size=12)
                    pdf.multi_cell(0, 10,txt=line.replace('* ', '-')+'\n')
            else:
                pass
                
    pdf.output(nome_arquivo +'.pdf')
    #Desenvolver mais        
    