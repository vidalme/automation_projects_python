
# Trem - Gerador de Usuários e Permissões (com relátorios)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-MIT-green)

<p>O script `trem.py` automatiza o cadastro de usuários, gerenciamento de permissões e geração de relatórios em sistemas Linux. <br>
Ele permite cadastrar novos usuários com base em dados de colaboradores armazenados em um arquivo XLS, separando-os por departamento e aplicando uma política mínima de segurança às senhas. 
<p>Além disso, o script tem a capacidade de gerar relatórios sobre os usuários do sistema, lista de todos os usuários cadastrados e lista de usuários de um grupo específico. 

Sinta-se à vontade para ajustar o script conforme necessário para atender às suas necessidades específicas.

## Instalação

Para usar este script, você precisará ter Python instalado em seu sistema e a biblioteca pandas.<br> <p>Você pode fazer o download e instalar o Python em [python.org](https://www.python.org/).
<p>Para instalação de panda pode usar o arquivo requirements.txt ou o gerenciador de pacotes pip.

## Uso

<h4>1. Clone o repositório:</h4>

```bash
git clone https://github.com/vidalme/trem.git
cd trem.py
```

<h4>2.Instale as dependências:</h4>

```bash
pip install -r requirements.txt
```

<h4>3.Execute o script abaixo para gerar um arquivo .xls com dados aleatorios para teste</h4>

```bash
python gera_colaboradores.py
```

<h4>4.O script com a flag '-add' extrai o conteudo do colaboradores.xls e adiciona todos os usuarios e grupos no sistema, a flag '-del' remove todos os usuarios e grupos que foram criados.</h4>

```bash
python trem.py -add 
```
```bash
python trem.py -del 
```
<h4>5.Para um relatorio com todos os usuarios cadastrados e seus grupos equivalentes use a flag -a ou --all-users</h4>
```bash
python trem.py --all-users
```

<p>O script irá automatizar o cadastro de usuários com base em dados armazenados em um arquivo .xls, gerenciar permissões de usuários e grupos, e permitir a geração de relatórios sobre os usuários do sistema.


## Opções de Linha de Comando

O script aceita as seguintes opções de linha de comando:

- `-a, --all-users`: Gera um relatório com a lista de todos os usuários.
- `-g, --all_groups GROUP`: Gera um relatório com todos os departamentos da empresa (grupos)
- `-gu, --group_users GROUP`: Gera um relatório com a lista de usuários de um grupo específico. O argumento GROUP especifica o nome do grupo.
- `-h, --help`: Exibe uma mensagem de ajuda com as opções disponíveis.