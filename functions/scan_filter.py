#Esse script filtra uma sainda em xml do comando NMAP em um host alvo
# Gerando IP, porta, serviço e versão
import xml.etree.ElementTree as ET


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
  