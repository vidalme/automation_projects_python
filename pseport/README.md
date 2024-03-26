# Pseport

<h4>Pseport é um script que automatiza a coleta de reports de processos ativos (ps -aux) e salva-los em um local apropriado.</h4>

<p>Nome: <b>pseport.py</b>

<p>Script que coleta todos os processos ativos do sistema e salva a lista em um arquivo localizado no diretorio "/tmp/reports". <p>

<p>O arquivo será salvo com a tag do dia, mes e ano que foi criado (a intenção é que rode em um cronjob diariamente). Porem pode tambem ser usado manualmente, basta chamar o script, quando usado manualmente ele envia mensagem com o resultado da operação.

Para criar o Cronjob:
```
$ crontab -e
```
<p>Adiciona no arquivo cron a linha abaixo para rodar o script todos os dias ao meio dia.

```
00 12 * * * /home/andre/bin/pseport.py
```
ou
```
@daily /home/andre/bin/pseport.py
```