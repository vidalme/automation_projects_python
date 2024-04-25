# Paratodos
![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-MIT-green)


<p> Programa para enviar por ssh múltiplos arquivos para uma lista de servidores definidos no arquivo server_list.txt


<p> O script precisa de python3 instalado e o módulo paramiko para fazer o upload dos arquivos de forma segura com ssh.


<p> Instalação:


```
$ sudo apt install python
```


```
$ pip install paramiko
```
<br>
<p>Após a instalação você pode usar normalmente com os parâmetros.


```
$ ./paratodos.py /local/diretorio_alvo/ /remote/diretorio_destino
```


<p>O script paratodos.py recebe dois argumentos, um path de destino e um path alvo, envia o conteúdo de um diretório local para todos os servidores listados no arquivo - 'servers_list.txt'.


<li>[ diretório alvo ]      Todos os arquivos desse diretório serão enviados para os servidores definidos.</li>
<li>[ diretório destino ]   Cada servidor remoto receberá os arquivos na pasta criada dentro da /home/USUARIO .
<br>
<br>
<br>


<p>Para ajuda digite -help


```
$ ./paratodos.py -help
```


<br>
<br>


    /// IMPORTANTE ///
    É necessário existir um arquivo chamado server_list.txt no mesmo diretório de onde está sendo rodado o script, esse arquivo vai conter uma lista com todos os IPs dos servidores que receberão os arquivos, esse arquivo deve ser alterado de acordo com a necessidade.


    A conexão é feita com ssh, então é necessário já haverem as permissões para os usuários se conectarem, assim como um usuário com esse nome criado no sistemas de destino.




<!--
Para criar o Cronjob:
```
$ crontab -e -->





