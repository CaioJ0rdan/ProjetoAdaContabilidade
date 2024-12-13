import boto3
import json
import zipfile
import os
import subprocess

# Lambda Configuration
lambda_function_name = "ProcessFile"
runtime = "python3.9"
role_name = "LambdaExecutionRole-S3-RDS"  # existing role
zip_file_name = "lambda_function.zip"
handler_name = "lambda_function.lambda_handler"
region = "us-east-1"
lambda_package_dir = "lambda_package"

# lambda_function.py :
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
    # Creating lambda_package
    if not os.path.exists(lambda_package_dir):
        os.makedirs(lambda_package_dir)
        print(f"Folder '{lambda_package_dir}' created.")

    # Creating lambda_function.py in the folder
    with open(f"{lambda_package_dir}/lambda_function.py", "w") as f:
        f.write(lambda_code)
    print(f"Archive 'lambda_function.py' created in '{lambda_package_dir}'.")

    # Install pymysql in lambda_package
    print(f"Instalando pymysql em '{lambda_package_dir}'...")
    subprocess.run(["pip", "install", "pymysql", "-t", lambda_package_dir], check=True)
    print("Dependências instaladas com sucesso.")

    # Criate the ZIP file
    print(f"Creating ZIP file '{zip_file_name}'...")
    with zipfile.ZipFile(zip_file_name, "w") as zipf:
        for root, dirs, files in os.walk(lambda_package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, lambda_package_dir))
    print(f"ZIP file '{zip_file_name}' created.")

def get_role_arn(role_name):
    try:
        iam_client = boto3.client("iam", region_name=region)
        print(f"Getting role ARN  '{role_name}'...")
        response = iam_client.get_role(RoleName=role_name)
        role_arn = response["Role"]["Arn"]
        print(f"ARN role '{role_name}': {role_arn}")
        return role_arn
    except Exception as e:
        print(f"Error to get ARN role '{role_name}': {e}")
        return None

def create_lambda_function(role_arn):
    lambda_client = boto3.client("lambda", region_name=region)

    try:
        print(f"Criating Lambda_function '{lambda_function_name}'...")
        with open(zip_file_name, "rb") as f:
            zip_content = f.read()

        response = lambda_client.create_function(
            FunctionName=lambda_function_name,
            Runtime=runtime,
            Role=role_arn,
            Handler=handler_name,
            Code={"ZipFile": zip_content},
            Description="lambda function to process files in S3 and save in RDS",
            Timeout=30,  # Time limit of 30 seconds
            MemorySize=128,  # Memory of 128 MB
            Publish=True
        )
        print(f"Lambda Function '{lambda_function_name}' created.")
        return response
    except Exception as e:
        print(f"Error to create lambda function: {e}")
        return None

if __name__ == "__main__":
    # Create a lambda package
    create_lambda_package()

    # Getting ARN of role 
    role_arn = get_role_arn(role_name)
    if not role_arn:
        print("Fail to get the ARN role.")
    else:
        print(f"Role ARN: {role_arn}")

        # Criar a função Lambda
        lambda_response = create_lambda_function(role_arn)
        if lambda_response:
            print("Lambda Configuration successfully completed!")
        else:
            print("Fail to create a  Lambda function.")
