# Esse script se conectar via ssh a um host linux
# E executa um comando para listar portas abertas
# Esse escript é só uma abstração!!!!
import paramiko, os, time
from colorama import init,Fore,Style
from dotenv import load_dotenv
import os, platform


load_dotenv()
user = os.getenv('USER_SSH')
passw = os.getenv('PASSWORD')

init(autoreset=True)

try:
    client = paramiko.SSHClient()
        
    # Carregar as chaves de host do sistema
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect('127.0.0.1','22',f'{user}',f'{passw}')

    stdin, stdout, stderr = client.exec_command(f'uname -s')
    saida = stdout.read().decode().strip()

    if saida == 'Linux':
        while True:
            if platform.system() == 'Linux':
                os.system('clear')  
            elif platform.system() == 'Windows':
                os.system('cls')

            stdin, stdout, stderr = client.exec_command(f'netstat -vlpt')
            print(stdout.read().decode())
            time.sleep(20)
    else:
        stdin, stdout, stderr = client.exec_command(f'ver')
        saida = stdout.read().decode().strip()
        if 'Windows' in saida:
            while True:
                if platform.system() == 'Linux':
                    os.system('clear')  
                elif platform.system() == 'Windows':
                    os.system('cls')

                stdin, stdout, stderr = client.exec_command(f'netstat -anr')
                print(stdout.read().decode())
                time.sleep(20)
                
except KeyboardInterrupt:
    client.close()

