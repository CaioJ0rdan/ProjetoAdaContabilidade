import boto3
import json
import zipfile
import os
import subprocess

# Configurações da Lambda
lambda_function_name = "ProcessFile"
runtime = "python3.9"
role_name = "LambdaExecutionRole-S3-RDS"  # Nome da role já criada
zip_file_name = "lambda_function.zip"
handler_name = "lambda_function.lambda_handler"
region = "us-east-1"
lambda_package_dir = "lambda_package"

# Código da função Lambda
lambda_code = """
import json
import boto3
import pymysql

# Configurações do banco RDS/MySQL
db_host = "adacontabilidade-rds.cz80y04yayed.us-east-1.rds.amazonaws.com"
db_user = "admin"
db_password = "MyPwd321"
db_name = "adacontabilidade"

# Clientes AWS
s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        print("Recebendo evento do S3...")
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        file_key = event['Records'][0]['s3']['object']['key']
        print(f"Bucket: {bucket_name}, Arquivo: {file_key}")

        # Ler o arquivo do S3
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        file_content = response['Body'].read().decode('utf-8')
        print("Arquivo lido com sucesso.")

        # Contar as linhas do arquivo
        lines = file_content.strip().split("\\n")
        num_lines = len(lines)
        print(f"Número de linhas no arquivo: {num_lines}")

        # Conectar ao banco de dados
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        print("Conexão ao banco de dados estabelecida com sucesso.")

        # Inserir dados no banco
        with connection.cursor() as cursor:
            sql = "INSERT INTO arquivos (nome_arquivo, numero_linhas) VALUES (%s, %s)"
            cursor.execute(sql, (file_key, num_lines))
            connection.commit()
        print("Dados inseridos no banco com sucesso.")

        return {
            'statusCode': 200,
            'body': f"Arquivo '{file_key}' processado com sucesso! Linhas: {num_lines}"
        }

    except Exception as e:
        print(f"Erro durante a execução da Lambda: {e}")
        return {
            'statusCode': 500,
            'body': f"Erro: {e}"
        }
"""

def create_lambda_package():
    # Criar a pasta lambda_package
    if not os.path.exists(lambda_package_dir):
        os.makedirs(lambda_package_dir)
        print(f"Pasta '{lambda_package_dir}' criada com sucesso.")

    # Criar o arquivo lambda_function.py dentro da pasta
    with open(f"{lambda_package_dir}/lambda_function.py", "w") as f:
        f.write(lambda_code)
    print(f"Arquivo 'lambda_function.py' criado em '{lambda_package_dir}'.")

    # Instalar pymysql na pasta lambda_package
    print(f"Instalando pymysql em '{lambda_package_dir}'...")
    subprocess.run(["pip", "install", "pymysql", "-t", lambda_package_dir], check=True)
    print("Dependências instaladas com sucesso.")

    # Criar o arquivo ZIP
    print(f"Criando o arquivo ZIP '{zip_file_name}'...")
    with zipfile.ZipFile(zip_file_name, "w") as zipf:
        for root, dirs, files in os.walk(lambda_package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, lambda_package_dir))
    print(f"Arquivo ZIP '{zip_file_name}' criado com sucesso.")

def get_role_arn(role_name):
    try:
        iam_client = boto3.client("iam", region_name=region)
        print(f"Obtendo ARN da role '{role_name}'...")
        response = iam_client.get_role(RoleName=role_name)
        role_arn = response["Role"]["Arn"]
        print(f"ARN da role '{role_name}': {role_arn}")
        return role_arn
    except Exception as e:
        print(f"Erro ao obter ARN da role '{role_name}': {e}")
        return None

def create_lambda_function(role_arn):
    lambda_client = boto3.client("lambda", region_name=region)

    try:
        print(f"Criando a função Lambda '{lambda_function_name}'...")
        with open(zip_file_name, "rb") as f:
            zip_content = f.read()

        response = lambda_client.create_function(
            FunctionName=lambda_function_name,
            Runtime=runtime,
            Role=role_arn,
            Handler=handler_name,
            Code={"ZipFile": zip_content},
            Description="Função Lambda para processar arquivos no S3 e salvar dados no RDS",
            Timeout=30,  # Tempo limite de 30 segundos
            MemorySize=128,  # Memória de 128 MB
            Publish=True
        )
        print(f"Função Lambda '{lambda_function_name}' criada com sucesso.")
        return response
    except Exception as e:
        print(f"Erro ao criar a função Lambda: {e}")
        return None

if __name__ == "__main__":
    # Criar o pacote Lambda
    create_lambda_package()

    # Obter ARN da role existente
    role_arn = get_role_arn(role_name)
    if not role_arn:
        print("Falha ao obter o ARN da role. Verifique se a role existe e tente novamente.")
    else:
        print(f"Role ARN: {role_arn}")

        # Criar a função Lambda
        lambda_response = create_lambda_function(role_arn)
        if lambda_response:
            print("Configuração da Lambda concluída com sucesso!")
        else:
            print("Falha ao criar a função Lambda.")
