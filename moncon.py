import requests, paramiko, os, time
from colorama import init,Fore,Style

init(autoreset=True)

try:
    client = paramiko.SSHClient()
        
    # Carregar as chaves de host do sistema
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect('127.0.0.1','22','carlos_','3003Oliveira@')

    while True:
        os.system('clear')
        stdin, stdout, stderr = client.exec_command(f'netstat -vlpt')
        print(stdout.read().decode())
        time.sleep(20)
except KeyboardInterrupt:
    client.close()

