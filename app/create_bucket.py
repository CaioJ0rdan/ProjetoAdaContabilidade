import boto3
import json

# Configurações
bucket_name = "bucket-adacontabilidade"  # Bucket S3 Name
region = "us-east-1"  
role_arn = "arn:aws:iam::507755385152:role/LambdaExecutionRole-S3-RDS-CJ"  # ARN of Lambda role 

# Cliente AWS
s3 = boto3.client("s3", region_name=region)

def create_bucket_with_policy(bucket_name, region):
    try:
        # Create the bucket.
        print(f"Create bucket '{bucket_name}' in region '{region}'...")
        s3.create_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' created.")

        # Add Policy to Bucket.
        print("Add policy to bucket...")
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

        # Convert Policy to Json.
        bucket_policy_json = json.dumps(bucket_policy)

        # Apply Policy in bucket.
        s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy_json)
        print("Policy apllied.")

        # Configurar CORS 
        print("Configure CORS to bucket...")
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
        print("CORS configure apllied.")

        print(f"Bucket configuration '{bucket_name}' succesfuly.")
    except Exception as e:
        print(f"Error in bucket creation or policy configurations: {e}")

# Execute the function
create_bucket_with_policy(bucket_name, region)
