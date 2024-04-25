#!/usr/bin/env python
# Autor: Andre Vidal Almeida
# https://github.com/vidalme
#
# v0.1
# - lê uma lista de servidores e se conecta a cada um deles com ssh
# - envia todo o conteúdo desejado a cada um dos servidores
#

import sys, os,subprocess
import paramiko

#help
def usage_message():
    print()
    print('''
###################################################################
|                                                                 |
|                    [[   paratodos.py   ]]                       | 
|                                                                 |
|        O script paratodos.py recebe dois argumentos,            |
|        um diretório alvo e um diretório destino.                |
|                                                                 |
|        O conteúdo do diretorio alvo é enviado para o            |   
|        diretório destino 'paratodos' os servidores              |
|        definidos no arquivo './servers_list.txt'.               |
|                                                                 |
|                                                                 |
###################################################################
          ''')
    print(f"Uso: ./paratodos.py [ diretório alvo ] [ diretório destino ]")
    print(f"")
    print(f'''[ diretório alvo ]      Todos os arquivos desse diretório serão 
                        enviados para os servidores definidos.''')
    print()
    print(f'''[ diretório destino ]   Cada servidor remoto receberá os arquivos na 
                        pasta criada dentro da /home/USUARIO . ''')
    print()
    sys.exit()

#diretório destino não existe ou está vazio
def no_files():
    print(f"O diretório [ {sys.argv[1]} ] não existe ou está vazio")
    usage_message()


# server_list.txt não existe ou está vazio
def no_servers(s):
    print(f"O arquivo {s} não existe ou está vazio")
    usage_message()

#main business logic
def paratodos():

    #arquivo que define os servidores que irão receber os arquivos
    SERVIDORES = "server_list.txt"

    # usuário que logará nos servidores
    USUARIO = "andre"

    #diretório dos arquivos a serem enviados
    dir_alvo = sys.argv[1]
    
    #diretório destino irá ser criado dentro de /home/USUARIO
    dir_destino = sys.argv[2]

    #checa se o diretorio alvo existe e não está vazio
    if not os.path.exists(dir_alvo) or not os.listdir(dir_alvo): no_files()
    
    #monta path do diretório alvo
    path_alvo = os.path.join(os.getcwd(),sys.argv[1])
    
    # #monta path do diretorio remoto 
    path_destino = f"/home/{os.path.join(USUARIO,dir_destino)}/"
    
    #lista de arquivos a serem enviados ja com seus paths completos
    arquivos = [ os.path.join(path_alvo,arq) for arq in os.listdir(path_alvo) ] 
    
    #coleta a lista de servidores que vao receber os arquivos
    with open(SERVIDORES,'r') as sl:
        #le o arquivo inteiro e recebe o valor em formato de string
        servers = sl.read()

        #checa se existem servidores na lista de servidores do arquivo source        
        if not servers: no_servers(SERVIDORES)

        # cria uma lista com os servidores
        servers = servers.splitlines()
        # print(servers)

    # loop servidores remotos
    for server in servers:
       
        #cria o cliente ssh e conecta com ele no servidor
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
       
        ssh.connect(hostname=server, username=USUARIO)
        
        # cria o cliente sftp
        sftp = ssh.open_sftp()

        # cria a pasta destino caso ainda não exista
        try: sftp.stat(path_destino)
        except IOError: sftp.mkdir(path_destino)
        # entra no diretorio destino
        sftp.chdir(path_destino)

        # loop todos os arquivos e os envia
        for item in arquivos:
            destino = os.path.basename(item)
            sftp.put(item,destino)

        sftp.close()
        ssh.close()


if __name__ == "__main__":
    # help
    if sys.argv[1] == "-h" or sys.argv[1] == "-help" or len(sys.argv)-1 <= 1:
        usage_message()
    else:
        pass
        #roda a logica
        paratodos()