# Paratodos 
![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-MIT-green)
<p> O script precisa de python3 instalado e também o modulo paramiko para fazer o upload dos arquivos de forma segura com ssh.
<p> Instalação:

```
$ sudo apt install python
```

```
$ pip install paramiko
```
<p>Após instalação você pode usar normalmente com os parametros.

```
$ ./paratodos.py /local/diretorio_envio/ /remote/diretorio_recebido
```

<p>O script paratodos.py recebe dois argumentos, um path de destino e um path alvo, envia o conteudo de um diretorio local para todos os servidores listados no arquivo - 'servers_list.txt'.
<p>Para ajuda digite -help

```
$ ./paratodos.py -help
```
<h3> Command [ path destino ] [ path alvo ]</h3>
<li>[ path destino ] :  path para o diretorio que tera seu conteudo enviado
<li>[ path alvo ] :     path destino onde sera enviado o conteudo (se nao existir o script deve criar o diretorio)</li><br>

<br>

    /// IMPORTANTE /// 
    É necessário existir um arquivo chamado server_list.txt no mesmo diretorio de onde esta sendo rodado o script, esse arquivo vai conter uma lista com todos os IPs dos servidores que receberão os arquivos, esse arquivo deve ser alterado de acordo com a necessidade.

    A conexão é feita com ssh, então é necessarsio ja haverem as permissões para os usuários se conectarem, assim como um usuario com esse nome criado no sistemas de destino.


<!--
Para criar o Cronjob:
```
$ crontab -e -->
