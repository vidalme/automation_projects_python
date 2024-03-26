#!/usr/bin/env python
import os, subprocess, time

file_name_ending = 'report.txt'

def pseport(saving_directory = '/tmp/reports_processes'):

    #captura os processos que estao rodando no momento
    b = subprocess.run(['ps','-ar'],capture_output=True)
    running_processes = b.stdout.decode()

    # cria um novo diretorio para salvar os reports, caso nao exista ainda
    # if saving_directory not in os.listdir(): os.mkdir(saving_directory)
    if not os.path.exists(saving_directory):
        print(f"O path {saving_directory} nao existe, vamos criar um")
        os.mkdir(saving_directory)
    
    #caputra o dia e cira uma var com a tag para o nome do arquivo
    time_tag = time.strftime("%y_%m_%d_%M%S")
    
    #nome completo do arquivo, com uma timestamp (apenas dia, mes e ano pois o script roda cron uma vez por dia)
    file_name_complete = f"{time_tag}_{file_name_ending}"
    
    # file_path_complete = os.path.join(f"{os.path.join(os.getcwd())}",saving_directory,file_name_complete)
    file_path_complete = os.path.join(saving_directory,file_name_complete)

    #abre o arquivo e poe o log dentro
    with open ( file_path_complete , 'w' ) as opened_file:
        opened_file.write(running_processes)
    
    # # mensagem para ficar facil para o usuario
    print(f"Seu arquivo {file_path_complete} foi salvo com sucesso")

# cotrole
if __name__ == "__main__":
    #variaveis ára o nome e local do arquivo de reports
    pseport()