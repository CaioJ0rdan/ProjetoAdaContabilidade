import boto3
import os
import random
import string

def generate_and_upload_to_s3(bucket_name, region="us-east-1", file_prefix="file"):
    """
    Generates a file with random size and content, and uploads it to an S3 bucket.
    
    :param bucket_name: Name of the S3 bucket to upload the file to.
    :param region: S3 bucket region (default is "us-east-1").
    :param file_prefix: Prefix for the file name (default is "file").
    """
    # Initialize S3 client
    s3 = boto3.client('s3', region_name=region)

    # Get the next file number by checking existing files
    file_number = 1
    while os.path.exists(f"{file_prefix}{file_number}.txt"):
        file_number += 1
    
    # Generate the new file name
    file_name = f"{file_prefix}{file_number}.txt"

    # Generate a random size for the file (1 KB to 1 MB)
    size_bytes = random.randint(1024, 2048)

    # Generate random content for the file
    content = ''.join(random.choices(string.ascii_letters + string.digits, k=size_bytes))

    # Create and write the content to the file
    with open(file_name, 'w') as file:
        file.write(content)
    
    print(f"File '{file_name}' generated with {size_bytes} bytes.")

    # Upload the file to the S3 bucket
    try:
        s3.upload_file(file_name, bucket_name, os.path.basename(file_name))
        print(f"File '{file_name}' successfully uploaded to S3 bucket '{bucket_name}'.")
    except Exception as e:
        print(f"Error uploading file to S3: {e}")


# Call of function 
if __name__ == "__main__":
    generate_and_upload_to_s3(bucket_name="bucket-adacontabilidade")
