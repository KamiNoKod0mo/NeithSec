# Esse script se comunica com a API do gemmini, gerando um resposta 
# que posteriomente sera usada na criação de pdf e scripts
import requests,os
from dotenv import load_dotenv

load_dotenv()

def ai_response(vuln):
    #url + chave API
    keys = os.getenv('KEYS')
    #print(keys)
    #keys = 'AIzaSyA1EJqNhbt1CXAPIbOCgRxfTcMBduQWImo'
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={keys}'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36",
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [{
            "parts": [{
                "text": f"Explique com 1000 palavras o que é e como funciona a {vuln} e como se proteger com comandos em ambientes Linux e Windows, com a resposta organiza em falando da vulnerabilidade, depois como se previnir no windows e depois no linux"
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
  