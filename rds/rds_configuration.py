import boto3
import time

# RDS Configurations
db_instance_identifier = "adacontabilidade-rds"
db_name = "adacontabilidade"
db_username = "admin"
db_password = "MyPwd321"
region = "us-east-1"

# RDS Client creation
rds_client = boto3.client("rds", region_name=region)

def create_rds_instance(security_group_id):
    try:
        print(f"Starting the creation of RDS instance '{db_instance_identifier}'...")
        
        # Create the RDS instance
        response = rds_client.create_db_instance(
            DBName=db_name,
            DBInstanceIdentifier=db_instance_identifier,
            AllocatedStorage=20,  # Storage size in GB
            DBInstanceClass="db.t3.micro",  # Free Tier-compatible instance class
            Engine="mysql",  # MySQL engine
            EngineVersion="8.0.33",  # Engine version compatible with the instance class
            MasterUsername=db_username,
            MasterUserPassword=db_password,
            Port=3306,  # Default MySQL port
            PubliclyAccessible=True,  # Publicly accessible (for testing purposes)
            BackupRetentionPeriod=7,  # Backup retention period in days
            MultiAZ=False,  # No high availability for testing
            StorageType="gp2",  # Standard SSD
            VpcSecurityGroupIds=[security_group_id],  # Previously configured Security Group
            DeletionProtection=False  # No deletion protection
        )

        # Display initial instance information
        print("RDS instance is being created. This might take a few minutes...")
        print("Initial information:")
        print(response)
        
        # Wait for the instance to become available
        waiter = rds_client.get_waiter('db_instance_available')
        waiter.wait(DBInstanceIdentifier=db_instance_identifier)
        print(f"RDS instance '{db_instance_identifier}' successfully created!")

        # Retrieve information about the created instance
        db_instance = rds_client.describe_db_instances(DBInstanceIdentifier=db_instance_identifier)
        endpoint = db_instance["DBInstances"][0]["Endpoint"]["Address"]
        print(f"Instance endpoint: {endpoint}")
        
        return endpoint

    except Exception as e:
        print(f"Error during the creation of the RDS instance: {e}")
        return None

def configure_security_group():
    try:
        ec2_client = boto3.client("ec2", region_name=region)
        print("Locating existing Security Group...")

        response = ec2_client.describe_security_groups(
            Filters=[
                {"Name": "group-name", "Values": ["RDSAccessGroup"]}
            ]
        )

        security_group_id = response["SecurityGroups"][0]["GroupId"]
        print(f"Security Group found with ID: {security_group_id}")
        return security_group_id
    except Exception as e:
        print(f"Error locating the existing Security Group: {e}")
        return None

if __name__ == "__main__":
    # Configure Security Group
    security_group_id = configure_security_group()

    if security_group_id:
        print(f"Security Group configured with ID: {security_group_id}")

        # Create the RDS instance and associate the Security Group
        rds_endpoint = create_rds_instance(security_group_id)
        if rds_endpoint:
            print(f"RDS instance successfully created! Endpoint: {rds_endpoint}")
        else:
            print("Failed to create the RDS instance.")
    else:
        print("Failed to configure the Security Group.")
