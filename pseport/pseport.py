#!/usr/bin/env python
# Autor: Andre Vidal Almeida
# https://github.com/vidalme
#
# v0.1
# - Coleta e loga informações dos processos do user atual (root quando estiver rodando com cron) 
# - salva com o rotulo da data mes e ano. 
# - script tem a intenção de rodar daily cron.
#

import os, subprocess, time

def pseport():

    #direotrios onde serao salvos os arquivos de log
    saving_directory = '/tmp/reports_processes'
    #o formato e/ou final do nome do arquivo
    file_name_ending = 'report.txt'

    #captura os processos que estao rodando no momento
    b = subprocess.run(['ps','-u'],capture_output=True)
    running_processes = b.stdout.decode()

    # cria um novo diretorio para salvar os reports, caso nao exista ainda
    if not os.path.exists(saving_directory): os.mkdir(saving_directory)
    
    #caputra o dia e cria o timestamp
    time_st = time.strftime("%y_%m_%d_%M%S")
    
    #nome completo do arquivo
    file_name_complete = f"{time_st}_{file_name_ending}"
    
    #nome completo do path para o arquivo
    file_path_complete = os.path.join(saving_directory,file_name_complete)

    # abre o arquivo e poe o log dentro
    with open ( file_path_complete , 'w' ) as opened_file:
        opened_file.write(running_processes)

if __name__ == "__main__":
    pseport()