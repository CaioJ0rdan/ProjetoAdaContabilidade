import boto3
import time

# Configurações do RDS
db_instance_identifier = "adacontabilidade-rds"
db_name = "adacontabilidade"
db_username = "admin"
db_password = "MyPwd321"
region = "us-east-1"

# Criação do cliente RDS
rds_client = boto3.client("rds", region_name=region)

def create_rds_instance(security_group_id):
    try:
        print(f"Iniciando a criação da instância RDS '{db_instance_identifier}'...")
        
        # Criar a instância do RDS
        response = rds_client.create_db_instance(
            DBName=db_name,
            DBInstanceIdentifier=db_instance_identifier,
            AllocatedStorage=20,  # Tamanho em GB
            DBInstanceClass="db.t3.micro",  # Classe de instância compatível com o Free Tier
            Engine="mysql",  # Motor MySQL
            EngineVersion="8.0.33",  # Versão compatível com a classe de instância
            MasterUsername=db_username,
            MasterUserPassword=db_password,
            Port=3306,  # Porta padrão do MySQL
            PubliclyAccessible=True,  # Acessível publicamente (para testes)
            BackupRetentionPeriod=7,  # Retenção de backup em dias
            MultiAZ=False,  # Sem alta disponibilidade para teste
            StorageType="gp2",  # SSD padrão
            VpcSecurityGroupIds=[security_group_id],  # Security Group configurado anteriormente
            DeletionProtection=False  # Sem proteção contra exclusão
        )

        # Exibindo informações da instância
        print("Instância RDS sendo criada. Isso pode levar alguns minutos...")
        print("Informações iniciais:")
        print(response)
        
        # Esperar a instância estar pronta
        waiter = rds_client.get_waiter('db_instance_available')
        waiter.wait(DBInstanceIdentifier=db_instance_identifier)
        print(f"Instância RDS '{db_instance_identifier}' criada com sucesso!")

        # Obter informações da instância criada
        db_instance = rds_client.describe_db_instances(DBInstanceIdentifier=db_instance_identifier)
        endpoint = db_instance["DBInstances"][0]["Endpoint"]["Address"]
        print(f"Endpoint da instância: {endpoint}")
        
        return endpoint

    except Exception as e:
        print(f"Erro durante a criação da instância RDS: {e}")
        return None

def configure_security_group():
    try:
        ec2_client = boto3.client("ec2", region_name=region)
        print("Localizando Security Group existente...")

        response = ec2_client.describe_security_groups(
            Filters=[
                {"Name": "group-name", "Values": ["RDSAccessGroup"]}
            ]
        )

        security_group_id = response["SecurityGroups"][0]["GroupId"]
        print(f"Security Group encontrado com ID: {security_group_id}")
        return security_group_id
    except Exception as e:
        print(f"Erro ao localizar o Security Group existente: {e}")
        return None

if __name__ == "__main__":
    # Configurar Security Group
    security_group_id = configure_security_group()

    if security_group_id:
        print(f"Security Group configurado com ID: {security_group_id}")

        # Criar a instância do RDS e associar o Security Group
        rds_endpoint = create_rds_instance(security_group_id)
        if rds_endpoint:
            print(f"Instância RDS criada com sucesso! Endpoint: {rds_endpoint}")
        else:
            print("Falha ao criar a instância RDS.")
    else:
        print("Falha ao configurar o Security Group.")
