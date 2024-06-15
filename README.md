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
1. Clone o repositório: `git clone https://github.com/KamiNoKod0mo/Neith.git`
2. Instale as dependências:
```bash
cd Neith
chmod +x setup_install.sh
./setup_install.sh
```
## Uso
```bash
chmod +x start.sh
./start.sh ip
```
![Screenshot from 2024-06-15 12-13-30](https://github.com/KamiNoKod0mo/NeithSec/assets/149252909/93f1ca93-3ee2-4b3c-b190-4affd04d6af1)

## Gerando o seguinte pdf

![Screenshot from 2024-06-15 12-15-22](https://github.com/KamiNoKod0mo/NeithSec/assets/149252909/55b4a01f-ad59-4322-ad20-59c539cb4db5)








