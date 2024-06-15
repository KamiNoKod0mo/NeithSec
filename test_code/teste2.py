import subprocess
import re

# Mapeamento de serviços para pacotes conhecidos
SERVICO_PACOTE_MAPA = {
    'ssh.service': 'openssh-server',
    'nginx.service': 'nginx',
    'apache2.service': 'apache2',
    # Adicione outros mapeamentos conforme necessário
}

def obter_servicos():
    # Executa o comando systemctl list-units --type=service --state=running para listar serviços em execução
    comando = ['systemctl', 'list-units', '--type=service', '--state=running']
    resultado = subprocess.run(comando, capture_output=True, text=True)
    return resultado.stdout

def obter_versao_pacote(pacote):
    # Tenta obter a versão do pacote usando dpkg-query (Debian/Ubuntu) ou rpm (Red Hat/Fedora)
    comando_dpkg = ['dpkg-query', '--showformat=${Version}', '--show', pacote]
    comando_rpm = ['rpm', '-q', '--queryformat', '%{VERSION}', pacote]

    try:
        resultado = subprocess.run(comando_dpkg, capture_output=True, text=True, check=True)
        return resultado.stdout.strip()
    except subprocess.CalledProcessError:
        pass

def obter_versao_ssh():
    # Obtém a versão do SSH usando o comando ssh -V
    comando = ['ssh', '-V']
    resultado = subprocess.run(comando, stderr=subprocess.PIPE, text=True)
    versao = re.search(r'OpenSSH_([\d.]+)', resultado.stderr)
    return versao.group(1) if versao else "Versão não disponível"

# Obtém a lista de serviços em execução
servicos = obter_servicos().splitlines()

# Processa cada serviço para extrair o nome e obter a versão
for linha in servicos:
    partes = linha.split()
    if len(partes) > 0:
        nome_servico = partes[0]
        if nome_servico in SERVICO_PACOTE_MAPA:
            nome_pacote = SERVICO_PACOTE_MAPA[nome_servico]
            if nome_servico == 'ssh.service':
                versao = obter_versao_ssh()
            else:
                versao = obter_versao_pacote(nome_pacote)
            
            print(f"Serviço: {nome_pacote} {nome_servico}")
            print(f"  Versão: {nome_pacote} {versao}")
            print()

