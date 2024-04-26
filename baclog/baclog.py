#!/usr/bin/env python

import os, sys, subprocess
import yaml

from fabric import Connection
from datetime import datetime

def usage_message():
    print()
    print('''
#############################################################################
         
                        [[   baclog   ]]
           
                Coleta multiplos logs de multiplos
                servidores remotos e salva localmente
         
    As configurações são definidas no arquivo --> // config.yaml //
                 
##############################################################################
          ''')
    print(f"NOME")
    print(f"        baclog")
    # print()
    # print(f"SYNOPSIS")
    # print(f"        baclog")
    print()
    print(f"DESCRIÇÃO")
    print("         O baclog é uma ferramenta para automatizar")
    print("         a coleta e backup de logs vindos de vários servidores.")        
    print("         Os servidores que terão logs coletados são definidos no arquivo")
    print("         de configuração 'config.yaml'")
    print("")
    print("         Todos os arquivos são organizados em uma estrutura de diretórios")
    print("         Cada diretório conterá logs de um servidor específico.")
    print("")
    print("         Os logs são separados em dois arquivos")
    print("               successful_logins    -> Conexões ssh feitas COM sucesso")
    print("               failed_logins        -> Conexões ssh feitas SEM sucesso")
    print("")
    print("         O arquivo final une todos os diretórios")
    print("         em um só grande arquivo tar.gz")
    print()
    print(f"OPÇÕES")
    print("         As opções são todas definidas no arquivo de configuração")
    print('')
    print("         As especificações do config.yaml são:")
    print('')
    print("         destino     : esse será o folder criado com todos os logs")
    print("         periodo     : número máximo de arquivos de backup que serão mantidos")
    print("                       os mais antigos são deletados automaticamente")
    print("         servers     : uma lista com todos os servidores a terem dados coletados")
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
        #arquivo de configuração 
        with open("config.yaml","r") as f:

            #dados de configuração
            config = yaml.safe_load(f)

            #seta configurações
            periodo = config['periodo']
            destino = config['destino']
            arquivo_comprimido_nome = f"{destino}.tar.gz"

            #diretórios separados para logs de sucesso e falhos
            sucesso_dir = "successful_logins"
            falho_dir = "failed_logins"

        #loop na lista de servidores
        for server in config['servers']:
            #settings
            user = server['user']
            ip = server['server_ip']
            name = server['name']
            chave = server['chave']
            
            #path especifico para o servidor da vez
            destino_remoto = os.path.join(destino,name)
            
            #paths para os diretorios dentro do servidor remoto
            sucesso_login_dir = os.path.join(destino_remoto,sucesso_dir)    
            falho_login_dir = os.path.join(destino_remoto,falho_dir)

            #cria nomes pros arquivos de backup com timestamp
            sucesso_login_arquivo = os.path.join(sucesso_login_dir,f"{time_stamp()}.txt")
            falho_login_arquivo = os.path.join(falho_login_dir,f"{time_stamp()}.txt")

            #confere se ja temos dados desse serividor
            if os.path.isfile(arquivo_comprimido_nome):
                #desconprime o arquivo para adicionarmos novos logs 
                subprocess.run(f"tar -xf {arquivo_comprimido_nome}",shell=True)
            else:
                #cria novo diretorios para esse servidor
                subprocess.run(f"mkdir -p {sucesso_login_dir} {falho_login_dir}", shell=True)

            #tenta conectar ao servidor
            try: 
                #conexão com o servidor da vez, generic.pem é a chave para os servidores
                conn = Connection(host=ip, connect_kwargs={"key_filename": chave }, user=user)

                # tenta encontrar logs de sucesso, se existirem
                # criamos um arquivo com os dados dentro do diretorio correspondente
                try:
                    successful_logins = conn.run(f"journalctl -q -S yesterday | grep -iE 'sshd:session'")
                    with open (sucesso_login_arquivo,"w") as sl: sl.write(successful_logins.stdout)
                except Exception as e:print(f"================>> {e}")

                # #tenta encontrar logs que falharam, se existirem
                # #criamos um arquivo com os dados dentro do diretorio correspondente
                try:
                    failed_logins = conn.run(f"journalctl -q -S yesterday | grep -iE 'sshd.+failed'")
                    with open (falho_login_arquivo,"w") as fl: fl.write(failed_logins.stdout)
                except Exception as e:print(f"================>> {e}")

            except Exception as e:print(f"================>> {e}")

            #checa se o numero total de backups salvos supera o maximo estipulado
            #caso supere, apagamos o mais antigo 
            if len(os.listdir(sucesso_login_dir)) > periodo:
                all_sl_files = [ os.path.join(sucesso_login_dir,f) for f in os.listdir(sucesso_login_dir) ]
                all_sl_files.sort()
                os.remove(all_sl_files[0])

            if len(os.listdir(falho_login_dir)) > periodo:
                all_fl_files = [ os.path.join(falho_login_dir,f) for f in os.listdir(falho_login_dir) ] 
                all_fl_files.sort()
                os.remove(all_fl_files[0])

            #arquiva todos os backups and comprime arquivo
        subprocess.run(f"tar -czf {arquivo_comprimido_nome} {destino}", shell=True)

    except Exception as e: print(f">>>>>>>>>> {e}")

    # #deleta todos os arquivos originais
    subprocess.run(f"rm -rf {destino}", shell=True)
    conn.close()

if __name__ == "__main__":
    
    #a função principal é chamada se não houverem argumentos
    if len(sys.argv) == 1: 
        main()
    elif sys.argv[1]=="-h" or sys.argv[1]=="--help": usage_message()
    else: print('-h ou --help para ter ajuda')

