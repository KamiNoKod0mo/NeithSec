# Esse script serve para ligar os script, servindo de ponto central
# Tal script sera substituido quando for desenvolvido a interface WEB
# Ele importa todas os arquivos da pasta function
# ele é executado em conjunto com monvirus e monconnection  atraves do start.sh que usa o tmux
# assim gerando uma especie de dashboard no terminal
# Receber parametros como:
    # Qual exploit database vc quer usar
    # um numeros limite de respostas
    # o arquivo xml scan do nmap
    # nome do arquivos de sainda
    # se não quer que apareça nada na tela

# Em um loop while ele printa o banner, chama scan_filter
# com a função main ele chama exploit_database
# com a funão display_info ele imprimi o resultado e chama ai_response, depois pdf_gen
# Para finalizar ele remove arquivos temporarios
# Depois espera por 50 secs para o proximo loop

# Modulos da Neith
from scan_filter import filtrar_hosts_nmap
from exploit_database import expliot_db
from ai_response import ai_response
from pdf_gen import output,merge_pdfs
#

import argparse,time, os
from colorama import init,Fore,Style
import pyfiglet
import platform 


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-s', action='store', help='select which database you want(exploit-db, )')
    parser.add_argument('-l', action='store', help='Limit of outputs for each databe search')
    parser.add_argument('-nf', action='store', help='Select nmap file')
    parser.add_argument('-w', action='store', help='Output file')
    parser.add_argument('-q', action='store_false', help='Quiet mode')

    args = parser.parse_args()
    if not (args.s or args.l or args.nf or args.w):
        parser.print_help()
        quit()

pdf_files = []

def display_infos(resposta):
    cont = 0
    if resposta.status_code == 200:
        conteudo = resposta.json()
        #print(conteudo)
        for item in conteudo['data']:
            try:
                vulns_dict[item['id']] = [
                    (f'\t{Fore.YELLOW}[*]{Style.RESET_ALL}',item['description'][1].replace('&lt;', '').replace('&#039;', '')),
                    (f'\t\t{Fore.GREEN}[*]{Style.RESET_ALL}','https://www.exploit-db.com/exploits/'+item['description'][0]),
                    (f'\t\t{Fore.YELLOW}[*]{Style.RESET_ALL}',item['type_id']),
                    (f'\t\t{Fore.YELLOW}[*]{Style.RESET_ALL}',item['platform_id']),
                    (f'\t\t{Fore.YELLOW}[*]{Style.RESET_ALL}',item['code'][0]['code_type'],item['code'][0]['code'])
                ]
            except:
                vulns_dict[item['id']] = [
                    (f'\t{Fore.YELLOW}[*]{Style.RESET_ALL}',item['description'][1].replace('&lt;', '').replace('&#039;', '')),
                    (f'\t\t{Fore.GREEN}[*]{Style.RESET_ALL}','https://www.exploit-db.com/exploits/'+item['description'][0]),
                    (f'\t\t{Fore.YELLOW}[*]{Style.RESET_ALL}',item['type_id']),
                    (f'\t\t{Fore.YELLOW}[*]{Style.RESET_ALL}',item['platform_id']),
                    (f'\t\t', " " ,'' ," ")
                ]
                
            if args.q:
                print(vulns_dict[item['id']][0][0],vulns_dict[item['id']][0][1],)

                print(vulns_dict[item['id']][1][0],vulns_dict[item['id']][1][1],)                        
   
                print(vulns_dict[item['id']][2][0],"Type:",vulns_dict[item['id']][2][1])
                
                print(vulns_dict[item['id']][3][0],'Plataform:',vulns_dict[item['id']][3][1]) 
                
                print(vulns_dict[item['id']][4][0],vulns_dict[item['id']][4][1]+vulns_dict[item['id']][4][2]) 
                
                vuln_explain = (ai_response(vulns_dict[item['id']][0][1]))
            if args.w:
                #Save name and link
                datas = vulns_dict[item['id']]
                #print(datas[0][1])
                pdf_files.append(output(args.w,datas,cont == int(args.l),vuln_explain,item['id']))
            else:
                #print(vuln_explain)
                pass
            if args.l:
                cont= cont +1
                if cont == int(args.l):
                    if args.w:
                        pdf_files.append(output(args.w,datas,cont == int(args.l), vuln_explain, item['id']))
                    else:
                        print(vuln_explain)
                    break;
        print('-'*122+"|")
    else:
        print("Erro ao enviar a requisição.")


vulns_dict = {}
def main (respostas):
    #for SO
    #print(respostas)
    if len(respostas) == 1:
        resposta = expliot_db(respostas[0])
        print(f'{Fore.RED}[*]{Style.RESET_ALL}',respostas[0])
        display_infos(resposta)
    #for Services 
    else:
        for index in range(len(respostas[1])):
            #print(respostas[1][index])
            if respostas[1][index]['product'] != '':
                resposta = expliot_db(respostas[1][index]['product']+ ' ' +respostas[1][index]['version'])
                
                print(f'{Fore.RED}[*]{Style.RESET_ALL}',respostas[1][index]['protocolo'] + " " + respostas[1][index]['porta'] + " : " + respostas[1][index]['product']+ ' ' +respostas[1][index]['version'])
                
                display_infos(resposta)


if args.nf:
    while True:
    
        if platform.system() == 'Linux':
            os.system('clear')  
        elif platform.system() == 'Windows':
            os.system('cls')

        init(autoreset=True)
        banner = pyfiglet.figlet_format('              Neith', font='slant')
        print(f"{Fore.BLUE} {banner}", end='')
        print(f"{Fore.BLUE} \t\t    Made by: Neith Security             Version: 2.5{Style.RESET_ALL}\n", end='')
        
        resposta = None
        if args.s == "exploit-db":
            respostas = filtrar_hosts_nmap(args.nf)
            #print(respostas)
            print('Server IP: ',respostas[0][0]['ip'])
            print('-'*122+"|")
            
            main([respostas[0][1]['so']])
            
            main(respostas)
               
            pdf_files_fi = list(set([pdf for pdf in pdf_files if pdf is not None])) # tira os nones
            
            pdf_files_fi.insert(0,'pdf_models/Neith Business Plan-1.pdf') #adicionar capa
            pdf_files_fi.append('pdf_models/Neith Business Plan-3.pdf') # adicionar contra capa
            
            merge_pdfs(pdf_files_fi,f'../result/{args.w}.pdf') #juntar tudo
            
            pdf_files_fi = list(set([pdf for pdf in pdf_files if pdf is not None])) #Voltar variavel inicial
            
            #apaga pdf temporarios
            if platform.system() == 'Linux':
                for item in pdf_files_fi:
                    os.system(f'rm {item}')
            elif platform.system() == 'Windows':
                for item in pdf_files_fi:
                    os.system(f'del {item}')
            
            
            #limpar variaveis de pdf
            pdf_files = []
            pdf_files_fi = []
            #pausa
            print('Press ctrl+b and d for exit')
            
            time.sleep(50)
            
            print('-'*122+"|")
            
            
        
        
