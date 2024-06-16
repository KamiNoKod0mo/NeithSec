## Neith Project

Finalizado o prototipo V1 do projeto de pesquisa neith.
Essa ferramenta Realiza as seguintes ações

- Realiza uma varredura intervalada no servidor alvo com Nmap
- Monitoramento de exploit para os serviços instalados no servidor alvo
- Monitoramento de arquivo em pasta selecionadas, com api do virustotal
- Monitoramento das conexões do servidor alvo
- Por meio da api do gemini gera um pdf com sugestões de como eliminar as vulnerabilidades do servidor alvo

## Índice

- [Instalação](#instalação)
- [Uso](#uso)

## Instalação
Clone o repositório: `git clone https://github.com/KamiNoKod0mo/NeithSec.git`
- Para Linux
1. Instale as dependências pelo script:
```bash
cd NeithSec/install-setup
chmod +x setup_install.sh
./setup_install.sh
```
- Para windows
Instale o OpenSSH, Python 3 e pip:
1. Baixe o instalador do Python 3 em https://www.python.org/downloads/ e instale.
2. Durante a instalação, certifique-se de marcar a opção "Adicionar Python ao PATH".
3. Abra o prompt de comando (digite "cmd" na barra de pesquisa do Windows e pressione Enter).
4. Para instalar o OpenSSH, digite:
```bash
powershell Add-WindowsCapability -Online -Name OpenSSH.Client
powershell Add-WindowsCapability -Online -Name OpenSSH.Server
```
5. Verifique se o Python 3 e o pip estão instalados corretamente digitando:
```bash
python --version
pip --version
```
Instale o tmux e o nmap:
1. Baixe o instalador do tmux para Windows em https://github.com/babun/babun, ou através do Chocolatey (se estiver instalado).
2. Baixe o instalador do nmap para Windows em https://nmap.org/download.html e siga as instruções de instalação.

Instale as dependências Python:
1. Abra o prompt de comando.
2. Navegue até o diretório onde está o seu arquivo requirement.txt.
3. Instale as dependências usando o pip:
```bash
python --version
pip install -r install-setup/requirement.txt
```

## Uso
```bash
chmod +x start.sh
./start.sh ip
```
![Screenshot from 2024-06-15 12-13-30](https://github.com/KamiNoKod0mo/NeithSec/assets/149252909/93f1ca93-3ee2-4b3c-b190-4affd04d6af1)

## Gerando o seguinte pdf

![Screenshot from 2024-06-15 12-15-22](https://github.com/KamiNoKod0mo/NeithSec/assets/149252909/55b4a01f-ad59-4322-ad20-59c539cb4db5)








