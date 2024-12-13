Ordem de Execução :
app/create_bucket
rds/rds_configuration
rds/create_database (manualmente executar no MySQL)
app/configurelambda 
Ativar Notificação de Evento no Bucket Manualmente
app/up_file_to_s3 (código que cria um arquivo e manda pro bucket)





app/

create_bucket.py -> Cria o bucket S3 e adiciona sua política

up_file_to_s3.py -> Cria um arquivo com tamanho aleatório entre 1024 e 2048 bytes e sobe para o bucket criado.

create_lambda.py -> Cria o serviço Lambda e cria uma pasta localmente para ser zipada com o conteudo de lambda_function e suas dependências.


rds/

rds_configuration.py -> Cria o RDS e configura seu grupom de segurança.

create_database.sql -> Cria a Estrutura de Database dentro do sql (executar manualmente dentro do ambiente MySql).

