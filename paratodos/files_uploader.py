#!/usr/bin/env python

import sys, os,subprocess
import paramiko

#chamada em caso de engano ou mal uso do script
def usage_message():
    print()
    print('''
#########################################################################  
          
                    [[   paratodos.py   ]]
          
        Script que recebe um diretorio local e envia todo seu 
        conteudo para outro diretorio remoto em uma lista de 
        servidores carregadas do arquivo -> // server_list.txt // 
                  
#########################################################################
          ''')
    print(f"Usage: Command [ path destino ] [ path alvo ]")
    print(f"")
    print(f'''[ path destino ]    --  O path do diretorio destino: todos os arquivos desse diretorio serao 
                        enviados para a lista de servidores que estão lsitadas no arquivo 
                        server_list.txt''')
    print()
    print(f'''[ path alvo ]       --  O path do diretorio alvo: cada servidor remoto recebera os arquivos na 
                        pasta do usuario $USUARIO/[path alvo], se esse diretorio não existir 
                        ele sera criado atuomaticamente''')
    print()
    sys.exit()

#chamada em caso de o diretorio nao existir ou estar vazio
def no_files():
    print(f"O diretorio [ {sys.argv[1]} ] não existe no local ou esta vazio")
    usage_message()

def no_servers(s):
    print(f"O arquivo {s} não existe no local ou esta vazio")
    usage_message()

#main business logic
def uploader():

    #arquivo com uma lista de ips, cada um representa 
    #um servidor remoto que ira receber os arquivos enviados
    SERVIDORES = "server_list.txt"

    #usuario para ssh na lista de serivdores
    #todos os servidores que forem receber arquivos 
    #precisam ter um usuario com esse nome exatamente
    USUARIO = "vidal"

    #primeiro parametro recebe o diretorio dos arqvuios a serem enviados
    arquivos_dir = sys.argv[1]
    
    #segundo parametro recebe o diretorio destino dentro de /home/USUARIO que ira receber os arqvuios
    diretorio_destino = sys.argv[2]

    #checa se o diretorio local passado no argumento existe e contem arquivos
    if not os.path.exists(arquivos_dir) or not os.listdir(arquivos_dir): no_files()

    #path completo do diretorio que tem os arquivos a serem enviados (apenas os arquivos sao enviados)
    source_dir = os.path.join(os.getcwd(),sys.argv[1])
    
    #path completo do diretorio remoto que recebera os arquivos do servidor local
    target_dir = f"/home/{os.path.join(USUARIO,diretorio_destino)}/"

    #lista de arquivos a serem enviados ja com seus paths completos
    arquivos = [ os.path.join(source_dir,arq) for arq in os.listdir(source_dir) ] 
    
    #coleta a lista de servidores que vao receber os arquivos
    with open(SERVIDORES,'r') as sl:
        #le o arquivo inteiro e recebe o valor em formato de string
        servers = sl.read()

        #checa se existem servidores na lista de servidores do arquivo source        
        if not servers: no_servers(SERVIDORES)

        # splita a string nas quebras de linha '\n' e insere cada parte splitada em uma lista
        servers = servers.splitlines()
    
    # entra em cada servidor na lista
    for server in servers:
       
        #create ssh client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
       
        # Connect to the server
        ssh.connect(hostname=server, username=USUARIO)
        
        # Create SFTP client
        sftp = ssh.open_sftp()

        # checa se a pasta destino existe, se nao, cria ela em cada servidor
        try: sftp.stat(target_dir)
        except IOError: sftp.mkdir(target_dir)

        # loop em todos os arquivos que serao enviados
        for item in arquivos:
            pass
            #sftp tem metodo para enviar e receber
            # sftp.put(item,os.path.join(target_dir,os.path.basename(item)))

            # print(f'''O arquivo {item} \n
            #        foi enviado para o servidor {server}\n
            #         com o nome {os.path.join(target_dir,os.path.basename(item))}
            #     ''')
            # print()
            # arquivo_enviado = subprocess.run(['scp', item , f"{USUARIO}@{server}:{target_dir}" ])

        #fechando as conexoes com o servidor
        sftp.close()
        ssh.close()

if __name__ == "__main__":

    # primeira coisa checar se o usuario quer ajuda
    if sys.argv[1] == "-h" or sys.argv[1] == "-help":
        usage_message()
    else:
        #roda a logica
        uploader()