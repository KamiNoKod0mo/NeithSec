# Importando os módulos necessários
from functions import *
import argparse,time, os
from colorama import init,Fore,Style
import pyfiglet


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
                output(args.w,datas,cont == int(args.l),vuln_explain)
            else:
                #print(vuln_explain)
                pass
            if args.l:
                cont= cont +1
                if cont == int(args.l):
                    if args.w:
                        output(args.w,datas,cont == int(args.l), vuln_explain)
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
        os.system('clear')
        init(autoreset=True)
        banner = pyfiglet.figlet_format('              Neith', font='slant')
        print(f"{Fore.BLUE} {banner}", end='')
        print(f"{Fore.BLUE} \t\t    Made by: Carlos             Version: 1.0{Style.RESET_ALL}\n", end='')
        
        resposta = None
        if args.s == "exploit-db":
            respostas = filtrar_hosts_nmap(args.nf)
            #print(respostas)
            print('Server IP: ',respostas[0][0]['ip'])
            print('-'*122+"|")
            
            main([respostas[0][1]['so']])
            
            main(respostas)   
                        
            print('Press ctrl+b and d for exit')
            time.sleep(25)
            print('-'*122+"|")
            
            
        
        
