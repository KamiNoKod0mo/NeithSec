# Esse script se conecta via ssh a um host, baixa os arquivos de pastas definidas
# Gera um hash md5 para monitorar a modifição de arquivos sanlvos em files_hash_virus.json
# Envia esse arquivos para  a API do virus total
# Mostrando a resposta em verder ou vermelho
import requests, paramiko, os, platform
from colorama import init,Fore,Style
import hashlib, json, time
from dotenv import load_dotenv

load_dotenv()
user = os.getenv('USER_SSH')
passw = os.getenv('PASSWORD')

#Diretorios a serem monitorados
dirs = ['teste1','teste2']
init(autoreset=True)


def connect(ip,port,user,password,up=0):
    arquivos = []
    client = paramiko.SSHClient()
    
    # Carregar as chaves de host do sistema
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Conectar ao servidor
        client.connect(ip, port, user, password)
        # Criar um objeto SFTP
        sftp = client.open_sftp()

        stdin, stdout, stderr = client.exec_command(f'uname -s')
        saida = stdout.read().decode().strip()

        if saida == 'Linux':

            for num in range(len(dirs)):
                stdin, stdout, stderr = client.exec_command(f'find {dirs[num]} -maxdepth 1 -type f')
                # Baixar o arquivo do servidor
                
                # Ler e imprimir a saída do comando
                arquivos.append(((stdout.read().decode()).strip("[]\n").split("\n")))
        else:
            stdin, stdout, stderr = client.exec_command(f'ver')
            saida = stdout.read().decode().strip()
            if 'Windows' in saida:
                for num in range(len(dirs)):
                    arquivosW = []
                    stdin, stdout, stderr = client.exec_command(f'dir /b {dirs[num]}')
                    # Baixar o arquivo do servidor
                
                    # Ler e imprimir a saída do comando
                    wi = (((stdout.read().decode().replace('\r','')).strip("[]\n").split("\n")))

                    for x in wi:
                        arquivosW.append(f'{dirs[num]}/{x}')
                    arquivos.append(arquivosW)
                    
        for x in range(len(dirs)):
            for arqs in range(len(arquivos[x])):
                nome_arquivo = os.path.basename(arquivos[x][arqs])
                #print(nome_arquivo)
                destino = os.path.join('tmp', nome_arquivo)
                
                sftp.get(arquivos[x][arqs], destino)
    finally:
        # Fechar a conexão
        sftp.close()
        client.close()
        return(arquivos)  


def analisy(arquivo):
    #print(arquivo)
    urlUp = "https://www.virustotal.com/api/v3/files"

    files = { "file": (f"{arquivo}", open(f"{arquivo}", "rb"), "image/png") }
    headers = {
        "accept": "application/json",
        "x-apikey": "c81c39f628831e4acc54f5337bb62dee0c1a25bad806f3c889ca64d462585bd9"
    }

    responseUp = requests.post(urlUp, files=files, headers=headers)
    #print(responseUp)
    dataUp = responseUp.json()
    id = dataUp["data"]['id']

    return id


def infos(id,arquivo):
    url = f"https://www.virustotal.com/api/v3/analyses/{id}"

    headers = {
        "accept": "application/json",
        "x-apikey": "c81c39f628831e4acc54f5337bb62dee0c1a25bad806f3c889ca64d462585bd9"
    }
    
    response = requests.get(url, headers=headers)
    data = response.json()
    #print(response.text)
    #print(data)
   
    analisy =(data['data']['attributes']['stats'])
    infos = (data['meta']['file_info'])
    
    color = 0
    if (data['data']['attributes']['stats']['malicious']) == 0:
        color = Fore.GREEN
    elif(data['data']['attributes']['stats']['malicious']) > 0:
        color = Fore.RED
    else:
        color = Fore.WHITE
        #Suspeito
    
    print(f"    {color}"+arquivo +f"{Style.RESET_ALL}")
    #print((data['data']['attributes']['stats']))
    #print((data['meta']['file_info']))
    
    
# Função para separar as strings
def separar_strings(lista):
    nova_lista = []
    for sublista in lista:
        nova_sublista = []
        for item in sublista:
            #print(item)
            if item == "/":
                nova_sublista = []
            else:
                nova_sublista.append(item)

        
        nova_lista.append(nova_sublista)
        #print(nova_sublista)
    return nova_lista


def calcular_md5(arquivo):
    """Calcula o hash MD5 de um arquivo."""
    hash_md5 = hashlib.md5()
    with open(arquivo, "rb") as f:
        for bloco in iter(lambda: f.read(4096), b""):
            hash_md5.update(bloco)
    return hash_md5.hexdigest()


def calcular_md5_dos_arquivos(diretorio):
    """Calcula o hash MD5 de todos os arquivos em um diretório."""
    resultados = {}
    
    try:
        md5 = calcular_md5(diretorio)
        resultados[diretorio] = md5
    except Exception as e:
        print(f"Erro ao calcular MD5 do arquivo {diretorio}: {e}")
    return resultados


def save_json(resultados, arquivo_json):
    with open(arquivo_json, 'w') as f:
        json.dump(resultados, f, indent=4)


try:
    if platform.system() == 'Linux':
        os.system('clear')  
    elif platform.system() == 'Windows':
        os.system('cls')

    save_json(None,'files_hash_virus.json')

    while True:
        #arquivo=(connect('127.0.0.1','22',f'{user}',f'{passw}'))
        arquivo=(connect('54.144.195.224','22','Administrator','B1!vrLyY@MoI@CIlRUFhTcR63-CD1ItU'))
        new_file = []
        new_files = []
        id = []
        hashmd5 = []
        p = 0
        
        
        for x in range(len(dirs)):
            new_file.append(separar_strings(arquivo[x]))
        #print(new_file)
        for x in range(len(dirs)):
            for y in range(len(new_file[x])):
                new_files.append(''.join([''.join(sublista) for sublista in (new_file[x][y])]))
        #print(new_files)
        for file in new_files:
            #print('tmp/' + file)
            
            hashmd5.append(calcular_md5_dos_arquivos('tmp/' + file))
        
        #print(hashmd5)
        try:          
            with open('files_hash_virus.json', "r") as f:
                # Carregando o conteúdo do arquivo JSON em um dicionário
                dados = json.load(f)
                #print(dados)
        except:
            pass
        

        #se o hash que estive armazenado em dados for igual a o novo hashmd5 entãao nao mandad para api
        try:
            for file in new_files:
                for hashs1,hashs2 in zip(dados,hashmd5):
                    #print(hashs1, '   ',hashs2)
                    #print('teste')
                    if (hashs1) == (hashs2):
                        p = p + 1
                    else:
                        id.append(analisy('tmp/'+file))
                        p = 0
        except:
            
            for file in new_files:
                id.append(analisy('tmp/'+file))
            
        save_json(hashmd5,'files_hash_virus.json')
        #####
        
        if len(id) >= 1 and p < len(id):
            if platform.system() == 'Linux':
                os.system('clear')  
            elif platform.system() == 'Windows':
                os.system('cls')
            #print(id)
            i = 0
            for x in range(len(dirs)):
                print(dirs[x]+"/")
                for y in range(len(arquivo[x])):
                    #print(id[i])         
                    infos(id[i],new_files[i])
                    i = i + 1

            if platform.system() == 'Linux':
                os.system('rm -fr tmp/*')  
            elif platform.system() == 'Windows':
                os.system('del tmp/*.*') 
              
except KeyboardInterrupt:
    pass
finally:
    
    if platform.system() == 'Linux':
        os.system('rm -fr tmp/*')  
    elif platform.system() == 'Windows':
        os.system('del tmp/*.*')

    save_json(None,'files_hash_virus.json')
