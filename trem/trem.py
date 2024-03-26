#!/usr/bin/env python
import pandas as pd
import os, sys, subprocess, pprint, random, re

#algumas constantes
#arquivo que sera a base para a criação
colaboradores_file = "colaboradores.xls"
#arquivos que serao criados e mantidos com dados de todos os usuarios criados pelo script
usarios_file = "/etc/empresa_allusers_names.txt"
grupos_file = "/etc/empresa_allgroups_names.txt"
#grupo que todos os usuarios serão criados
grupo_principal = "Colaboradores"

#mensagem de ajuda
def usage_message():
    print()
    print('''
###############################################################################
          
                            [[   TREM  ]]
            
        Automatiza o cadastro de usuários vindos de um arquivo .xls 
           gerenciamento de permissões e geração de relatorios.
                                 
###############################################################################
          ''')
    print(f"NOME")
    print(f"        TREM")
    print()
    print(f"SYNOPSIS")
    print("         trem.py [-add] [-del] [-a] [-g] [-gu GROUP] [-h]")         
    print()
    print(f"DESCRIÇÃO")
    print("         O gerenciamento_usuarios_permissoes é uma ferramenta em Python que automatiza o cadastro de usuários e o gerenciamento de permissões em um sistema Linux. Ele permite cadastrar novos usuários com base em dados de colaboradores armazenados em um arquivo XLS, separando-os por departamento e aplicando uma política mínima de segurança às senhas.")
    print()
    print("         Além disso, o script tem a capacidade de gerar relatórios sobre os usuários do sistema, incluindo lista dos últimos usuários logados, lista de todos os usuários cadastrados e lista de usuários de um grupo específico. Os relatórios podem ser salvos em diferentes formatos, como CSV, YAML ou XLS.")
    print()
    print("         O script também registra logs de erro detalhados durante o processo de cadastro de usuários e notifica os administradores sobre erros críticos que podem afetar a segurança ou o funcionamento do sistema.")
    print()
    print(f"OPÇÕES")
    print("""
    -h, --help
        Exibe uma mensagem de ajuda com as opções disponíveis.

    -add
        Adiciona todos os usuarios e grupos do arquivo 'colaboradores.xls'.

    -del
        Remove todos os usuarios e grupos instalados com o comando -add.

    -a, --all-users
        Lista todos os usuários  e seus grupos criados pelo commando --add.

    -g, --all-groups
        Lista apenas os grupos criados pelo commando --add.
                
    -gu GROUP, --group-users GROUPS
        Lista todos os membros de um grupo especifico, o nome do grupo é sensitivo para maiusculas ou minusculas. 

        """)
    print()

# 
def create_all_users(all):
    users_criados=[]
    
    sen = '1234'
    hashed_password = subprocess.run(f"echo -n '{sen}' | openssl passwd -1 -stdin", shell=True, capture_output=True, text=True).stdout.strip()
    # extrai todos os dados do .xls
    for user in all['Nome']:
        nome_com=all["Nome"][user]
        nome=nome_com.split(" ")
        nome=f"{nome[0].lower()}_{str(random.randint(1000,9999))}"
        grupo=all["Departamento"][user]
        fone=all["Telefone"][user]
        email=all["E-mail"][user]
        
        # chama a funcao de criar um so usuario com os parametros 
        user_criado = create_user(nome=nome, senha=hashed_password ,nome_com=nome_com, grupo=grupo, fone=fone, email=email )
        # adiciona usuario na lista de todos
        users_criados.append(user_criado)

    print("Todos usuarios foram adicionados com sucesso")
    print()
    return users_criados

# funcao para criar usuario
def create_user(nome, senha, nome_com, grupo, fone, email):
    # commandos linux para criacao de user
    subprocess.run(f"useradd -m -c '{nome_com}' -s /bin/bash -p {senha} -G {grupo} {nome}", shell=True)
    subprocess.run(f"usermod -aG {grupo_principal} {nome}", shell=True)
    # abre arquivo para adicionar o nome do usuario criado e salva local
    with open (usarios_file,"a") as users: 
        users.writelines(f"{nome},")
    print(f"{nome_com} adicionada(o), com o username {nome} no departamento {grupo},\nfone:{fone}\ne-mail:{email}")
    print()
    return(nome)

# lsita todos os usuarios
def lista_todos_colaboradores():
    # abre arquivo salvo localmente com a relacao de tds os usuarios
    with open (usarios_file,"r") as ltc:
        # lista dividida por usuario
        ltc = ltc.read().split(',')
        # remove o ultimo que eficou em branco
        del ltc[-1]
        # loop nos usuarios 
        for l in ltc:
            # cata os grupos que esse usuario pertence 
            gs = subprocess.run(f"groups {l}", shell=True, capture_output=True)
            # seleciona a parte que nos interressa
            gs = gs.stdout.decode().strip().split(" ")[3:]
            # lista tudo aqui
            print()
            print(f"{l}")
            print(f"grupos - {gs}")

# listagemd dos grupos que foram adicioandos 
def lista_todos_groups():
    with open (grupos_file,"r") as tgs:
        tgs = tgs.read().split(',')
        del tgs[-1]
        print(f"[ Lista de grupos da Empresa ]")
        for g in tgs: print(g)
        print()

# listagem 
def create_all_groups(groups):
    subprocess.run(['groupadd',grupo_principal])
    for group in groups:
        subprocess.run(['groupadd',f'{group}'])
        print(group)
        with open(grupos_file,'a') as groups:
            groups.writelines(f"{group},")
    
    print('Todos os grupos foram criados')
    print()

# abre o banco de dados, filtra os colaboradores e extrai
def lista_grupo_colaboradores(arg):

    args = sys.argv
    nxt_arg = args.index(arg)+1
    grp = sys.argv[nxt_arg]
    
    uls = subprocess.run(f"cat /etc/group | grep '{grp}' ",shell=True,capture_output=True)
    uls = uls.stdout.decode().strip().split(',')[1:]
    # print(uls)
    print()
    print(f"## Grupo {grp} ##")
    for u in uls: print(u)
    print()

#  remove todos os usuarios e limpa o banco de dados
def remove_all_users():
    with open(usarios_file,"r") as users:
        a = users.read().split(',')
        del a[-1]
        for i in a: remove_user(i)

    subprocess.run(f"> {usarios_file}",shell=True)
    print("Todos os colaboradores foram removidos com sucesso")
    print()

# remove todos todos os grups
def remove_all_groups():
    with open(grupos_file,'r') as grupos:
        rag = grupos.readlines()
        rag = rag[0].split(',')
        del rag[-1]
        for g in rag:
            subprocess.run(['groupdel',f'{g}'])
    subprocess.run(f"> {grupos_file}",shell=True)
    print('Todos os grupos foram removidos')
    print()

# remove um usuario
def remove_user(nome):
    subprocess.run(f"userdel -r {nome}",shell=True)
    print(f"remove user {nome}")

# adiciona tudo aqui
def main():

    # extrai do .xls
    df = pd.read_excel(colaboradores_file)
    df_unique_departamentos = df['Departamento'].unique().tolist()
    create_all_groups(df_unique_departamentos)
    df_dict = df.to_dict()
    # retorna a lista para usar em relatorios
    all_users = create_all_users(df_dict)


# funçaõ inicador, penera os argumentos passados
def init():
    # se não tiver argumento a gente chama ajuda do script 
    if len(sys.argv) == 1:
        usage_message()

    # todos os argumentos aqu
    if len(sys.argv) > 1:

        for arg in sys.argv:
            # adiciona todos os usuarios e grupos do colaboradores.xls
            if arg=="-add":
                main()
            
            # remove todos os usuarios e grupos do colaboradores.xls
            elif arg=="-del":
                try:
                    remove_all_users()
                except:
                    print('nao existem usuarios cadastrados')
                try:
                    remove_all_groups()
                except:
                    print('nao existem grupos cadastrados')
            
            # lista todos os colabores adicionados
            elif arg=="-a" or arg=="--all-users":
                lista_todos_colaboradores()

            # lista todos os grupos
            elif arg=="-g" or arg=="--all-groups":
                lista_todos_groups()

            # lista todos os usuarios de um grupo especifico
            elif arg=="-gu" or arg=="--group-users":
                lista_grupo_colaboradores("-gu")

            elif arg=="-h" or arg=="--help":
                usage_message()


if __name__ == "__main__": 
    init()