import boto3
import json

# Configurações
bucket_name = "bucket-adacontabilidade"  # Substitua por um nome único
region = "us-east-1"  # Substitua pela sua região (exemplo: us-east-1)
role_arn = "arn:aws:iam::507755385152:role/LambdaExecutionRole-S3-RDS-CJ"  # Substitua pelo ARN da role da Lambda

# Cliente AWS
s3 = boto3.client("s3", region_name=region)

def create_bucket_with_policy(bucket_name, region):
    try:
        # Criar o bucket
        print(f"Criando o bucket '{bucket_name}' na região '{region}'...")
        s3.create_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' criado com sucesso.")

        # Adicionar política ao bucket
        print("Adicionando política ao bucket...")
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": "lambda.amazonaws.com"},
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*"
                }
            ]
        }

        # Converter a política para JSON
        bucket_policy_json = json.dumps(bucket_policy)

        # Aplicar a política ao bucket
        s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy_json)
        print("Política aplicada com sucesso.")

        # Configurar CORS (se necessário)
        print("Configurando CORS para o bucket...")
        cors_configuration = {
            "CORSRules": [
                {
                    "AllowedOrigins": ["*"],
                    "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
                    "AllowedHeaders": ["*"]
                }
            ]
        }
        s3.put_bucket_cors(Bucket=bucket_name, CORSConfiguration=cors_configuration)
        print("Configuração de CORS aplicada com sucesso.")

        print(f"Configuração do bucket '{bucket_name}' concluída.")
    except Exception as e:
        print(f"Erro ao criar o bucket ou configurar políticas: {e}")

# Executar a função
create_bucket_with_policy(bucket_name, region)
