# baclog

![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-MIT-green)

<p><b>baclog</b> é uma ferramenta em Python para automatizar a coleta, organização e backup dos logs de multiplos servidores remotos.

<p> O script precisa de python3 e o módulo fabric instalados.

## Descrição

Este script automatiza o processo de coleta de logs de servidores remotos listados em um arquivo de configuração YAML e os salva localmente em um diretório separados com base em qual servidor os dados vieram. Os logs são compactados em um arquivo tar.gz para fácil armazenamento e transporte.

## Pré-requisitos

- Python 3.x
- Fabric (instalável via `pip install fabric`)

## Instalação

<h4>1. Clone o repositório:</h4>

```bash
git clone https://github.com/vidalme/baclog.git
cd baclog
```

<h4>2.Instale as dependências:</h4>

```bash
pip install -r requirements.txt
```

<h4>3.Re-defina o arquivo config.yaml com as informações dos servidores e as opções desejadas:</h4>

<p>O arquivo config.yaml contém as seguintes opções:

<b>destiny:</b> Diretório local onde os logs serão salvos.<br>
<b>period:</b> Número máximo de arquivos de backup que serão mantidos.<br>
<b>servers:</b> Lista de servidores remotos e suas configurações.<br>
<p>É possível adicionar quantos servidores quiser na lista.
<p>Exemplo de config.yaml:

```yaml
destiny: "/path/to/backups"
period: 5
servers:
  - name: "server1"
    user: "user1"
    server_ip: "192.168.1.101"
  - name: "server2"
    user: "user2"
    server_ip: "192.168.1.102"
  - name: "server3"
    user: "user3"
    server_ip: "192.168.1.103"   
```

<h4>4.Contribuindo:</h4>
<p>PRs são bem-vindos.

<h4>5.Licença:</h4>
<p>Este projeto está sob a Licença MIT - consulte o arquivo LICENSE para mais detalhes.
