# Esse script e chamda no arquivo index onde o mesmo chama a função output que delimita a saida e a organiza em uma lista
# Passando para função salvar_em_pdf que salvara em um templete configurado a saida do arquivo ai_responde através do ai_response
# No final com merge_pdf juntando tudo e salvando
import re, os
from fpdf import FPDF
import PyPDF2
import os



infos = []
def output(path,data,vf,vuln_explain,id):
    global infos
    infos = [] 
    infos.append([f'{data[0][1]}\n',f'\t{data[1][1]}\n',f'{vuln_explain}\n\n'])
    #print(vf)
    if vf == False:
        #print(infos)
        file = salvar_em_pdf(infos,path,id)
        return file 
      


def salvar_em_pdf(texto, nome_arquivo,id):
    padrao = r"\*\*(.*?)\*\*"
    pdf = FPDF()
    pdf.add_page()
    #print(texto)
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(255, 255, 255)
    
    pdf.image('pdf_models/model3.png',x=0,y=0,w=210, h=297)
    #print(infos)
    for i in range(0,len(texto)):
        
        
        pdf.set_font("Arial", style='B', size=14)
        pdf.cell(0, 10, txt=infos[i][0].replace('\n\n', '\n'),ln=True, align='C')
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(0, 10, txt=infos[i][1].replace('\n\n', '\n'),ln=True, align='C')
        pdf.set_font("Arial", size=12)
        

        pdf.set_y(30)
        for line in infos[i][2].splitlines():
            #print(line)
            #for te in range(len(line)):
                #print(line[te],end='')
            if pdf.get_y() > 248:
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.set_text_color(255, 255, 255)
    
                pdf.image('pdf_models/model3.png',x=0,y=0,w=210, h=297)
                pdf.set_y(20)
            if line.strip():
                if re.search(padrao, line):
                    pdf.ln()
                    pdf.set_font("Arial", style='B', size=12)
                    pdf.multi_cell(0, 10,txt=line.replace('**', '').replace('* ', '- ').replace('\n\n', '\n'))
                    #pdf.ln()
                #elif re.search()
                else:
                    pdf.set_font("Arial", style='',size=12)
                    pdf.multi_cell(0, 10,txt=line.replace('* ', '- ').replace('\n\n', '\n'))
            else:
                pass
           
            
                
        pdf.output(f'{nome_arquivo}{id}.pdf')
        
        return f'{nome_arquivo}{id}.pdf'
      

def merge_pdfs(pdf_files, nome_arquivo_saida):
    pdf_merger = PyPDF2.PdfMerger()
    
    for pdf in pdf_files:
        if os.path.exists(pdf):
            pdf_merger.append(pdf)
        else:
            print(f"Arquivo não encontrado: {pdf}")
    
    with open(nome_arquivo_saida, 'wb') as f_saida:
        pdf_merger.write(f_saida)
    
    pdf_merger.close()