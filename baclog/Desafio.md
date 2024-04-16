<h1>Automatizar Backup de Logs com Python</h1>

<h3>Cenário</h3>

<p>Você gerencia uma frota de servidores web que geram logs críticos.<br>
Você precisa automatizar o processo de backup desses logs diariamente, com recursos como:

<ul>

<li><b>Backups Rotativos:</b><br>
Manter apenas 7 backups diários no máximo (deletar o mais antigo).

<li><b>Compressão:</b><br>
Compactar os arquivos de log antes do backup para economizar espaço de armazenamento.

<li><b>Armazenamento Remoto:</b><br> 
Carregar os backups compactados para um servidor remoto (por exemplo, servidor SFTP) para segurança.

<li><b>Tratamento de Erros:</b><br>
Implementar o tratamento de erros para capturar e relatar problemas durante o processo de backup (por exemplo, falhas de conexão, problemas de espaço em disco).

<li><b>Registro:</b><br> 
Implementar a funcionalidade básica de registro para rastrear a execução do script e erros potenciais.

</ul>


<h3>Requisitos</h3>
<ul>
<li>Usar Python para escrever o script.
<li>Aproveitar bibliotecas para manipulação de arquivos, compressão (por exemplo, gzip), transferência remota de arquivos (por exemplo, paramiko para SFTP) e registro (por exemplo, módulo de registro).
<li>Configurar o script para aceitar argumentos ou ler configurações de um arquivo de configuração para detalhes como:
<ul>
<li>Localização dos diretórios de log nos servidores.
<li>Número de backups a serem retidos.
<li>Detalhes do servidor remoto (endereço, nome de usuário, senha/chave).
<li>Implementar um mecanismo de agendamento (fora do script) para executar o script de backup diariamente (por exemplo, cronjob no Linux).
</ul>
</ul>


<h3>Desafio</h3>
<p><b>Considere os casos em que:</b>
<ul>
<li>O que acontece se não houver logs para backup em um dia específico?
<li>Como você lidará com situações em que o servidor remoto está inacessível?
<li>Explore técnicas para operações atômicas durante a manipulação de arquivos e processos de backup para garantir a integridade dos dados.
<li>Pense em implementar um sistema de notificação para alertá-lo sobre qualquer falha de backup.
</ul>

<h3>Bônus</h3>
<ul>
<li>Estenda o script para lidar com diferentes formatos de log (por exemplo, backups separados para diferentes tipos de log).
<li>Integre-se com um provedor de armazenamento em nuvem (por exemplo, AWS S3) para backups remotos.
</ul>