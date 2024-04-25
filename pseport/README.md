# Pseport
![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-MIT-green)


<p>É necessário instalar o python 3 ou superior para usar esse script
<p>Nome: <b>pseport.py</b>

<h4>O Pseport automatiza a coleta de logs dos processos referentes ao $USER logado no sistema.</h4>
<p>Script que coleta todos os processos ativos do sistema e salva a lista em um arquivo localizado no diretório "/tmp/reports". <p>

<p>O arquivo será salvo com a tag do dia, mês e ano que foi criado (a intenção é que rode em um cronjob diariamente). Porém pode também ser usado manualmente, basta chamar o script ele coletará e armazenará com o nome apropriado os processos do $USER no momento que for chamado.

Para criar o Cronjob:
```
$ crontab -e
```
<p>Adicione no arquivo cron a linha abaixo para rodar o script todos os dias ao meio dia.

```
00 12 * * * [path para o script]
```
ex
```
@daily /home/andre/bin/pseport.py
```

