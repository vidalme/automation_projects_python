#!/usr/bin/env python

import os, sys, subprocess
import yaml

from fabric import Connection
from datetime import datetime

def usage_message():
    print()
    print('''
################################################################################### 
          
                         [[   baclog   ]]
            
                Coleta multiplos logs de multiplos servidores remotos 
                                e salva localmente 
          
            As configurações são carregadas do arquivo --> // config.yaml // 
                  
###################################################################################
          ''')
    print(f"NOME")
    print(f"        baclog")
    # print()
    # print(f"SYNOPSIS")
    # print(f"        baclog")
    print()
    print(f"DESCRIÇÃO")
    print("         O baclog é uma ferramenta para automatizar")
    print("         a coleta e backup de logs vindos de uma lista de servidores.")         
    print("         Os servidores que terão logs coletados estão listados no arquivo")
    print("         de configuração 'config.yaml' que deve residir no mesmo local")
    print("         que o script que esta rodando.")
    print("         Todos os arquivos são organizados em uma estrutura de folders")
    print("         Separados por servidor e logins de sucesso e falhas.")
    print("         O arquivo final junta todos os diretorios em um")
    print("         so e comprime em um arquivo tar.gz")
    print()
    print(f"OPÇÕES")
    print("         As opções foram todas colocadas no arquivo de configuração")
    print("         pois esse script foi criado com a intenção de rodar como um")
    print("         cronjob.")
    print("         As especificações do config.yaml são:")
    print("         destiny: esse sera o folder criado com todos os logs")
    print("         periodo: numero maximo de arquivos de backup que serão mantidos")
    print("                  os mais antigos são deletados automaticamente")
    print("         servers: uma lista com todos os servidores a terem dados coletados")
    print()

# função para criar um timestap para incluir no nome dos arquivos
def time_stamp():
    t = datetime.now()
    ano = t.strftime("%Y")
    mes = t.strftime("%m")
    dia = t.strftime("%d")
    hora = t.strftime("%H")
    minuto = t.strftime("%M")
    segundo = t.strftime("%S")
    # time_label = f"{ano}{mes}{dia}_{hora}-{minuto}---{segundo}_"
    time_label = f"{ano}-{mes}-{dia}__"
    return time_label

def main():
    try:  
        #abrir arquivo de configuração e criar as variaveis necessarias
        with open("config.yaml","r") as f:

            #carrega dados do arquivo de configuracoes
            config = yaml.safe_load(f)

            #settings
            max_acumulado = config['period']
            destiny = config['destiny']
            comp_file_name = f"{destiny}.tar.gz"

            #diretorios separados para logs de sucesso e falhos
            sl_fol = "successful_logins"
            fl_fol = "failed_logins"

        #loop na lista de servidores
        for server in config['servers']:
            
            #settings
            user = server['user']
            ip = server['server_ip']
            name = server['name']
            
            #path especifico para o servidor da vez
            destiny_plus = os.path.join(destiny,name)

            #paths para os diretorios dentro do servidor remoto
            sl_dir = os.path.join(destiny_plus,sl_fol)    
            fl_dir = os.path.join(destiny_plus,fl_fol)    

            #cria nomes pros arquivos de backup com timestamp
            sl_filename = os.path.join(sl_dir,f"{time_stamp()}.txt")
            fl_filename = os.path.join(fl_dir,f"{time_stamp()}.txt")

            #confere se ja temos dados desse serividor
            if os.path.isfile(comp_file_name):
                #deconprime o arquivo para adicionarmos novos logs 
                subprocess.run(f"tar -xf {comp_file_name}",shell=True)
            else:
                #cria novo diretorios para esse servidor
                subprocess.run(f"mkdir -p {sl_dir} {fl_dir}", shell=True)

            #tenta conectar ao servidor
            try: 
                conn = Connection(host=f"{user}@{ip}")
                 
                #tenta encontrar logs de sucesso, se existirem
                #criamos um arquivo com os dados dentro do diretorio correspondente
                try:
                    successful_logins = conn.run(f"journalctl -q -S yesterday | grep -iE 'sshd:session'")
                    with open (sl_filename,"w") as sl: sl.write(successful_logins.stdout)
                except Exception as e:print(f"================>> {e}")

                #tenta encontrar logs que falharam, se existirem
                #criamos um arquivo com os dados dentro do diretorio correspondente
                try:
                    failed_logins = conn.run(f"journalctl -q -S yesterday | grep -iE 'sshd.+failed'")
                    with open (fl_filename,"w") as fl: fl.write(failed_logins.stdout)
                except Exception as e:print(f"================>> {e}")
            except Exception as e:print(f"================>> {e}")

            #checa se o numero total de backups salvos supera o maximo estipulado
            #caso supere, apagamos o mais antigo 
            if len(os.listdir(sl_dir)) > max_acumulado:
                all_sl_files = [ os.path.join(sl_dir,f) for f in os.listdir(sl_dir) ]
                all_sl_files.sort()
                os.remove(all_sl_files[0])

            if len(os.listdir(fl_dir)) > max_acumulado:
                all_fl_files = [ os.path.join(fl_dir,f) for f in os.listdir(fl_dir) ] 
                all_fl_files.sort()
                os.remove(all_fl_files[0])

            #arquiva todos os backups and comprime arquivo
            subprocess.run(f"tar -czf {comp_file_name} {destiny}", shell=True)

    except Exception as e: print(f">>>>>>>>>> {e}")

    #deleta todos os arquivos originais
    subprocess.run(f"rm -rf {destiny}", shell=True)
    conn.close()

if __name__ == "__main__":

    #checa se o usuario precisa de ajuda
    try:
        if sys.argv[1]=="-h" or sys.argv[1]=="--help":
            usage_message()
        else:
            print('-h ou --help para ter ajuda')
    except Exception as e:
        print(f"================>> {e}")

    #a função principal é chamada se não tiverem argumentos
    if len(sys.argv) == 1:
        main()