# **AWS Automation Project - File Processing with S3, Lambda, and RDS**

This project implements an automated solution using AWS to process files uploaded to an S3 bucket and save information in an RDS database through a Lambda function.

---

## **Execution Order**

1. **Create S3 Bucket**
   - Run the `app/create_bucket.py` script to create the S3 bucket and configure its access policy.

2. **Configure RDS**
   - Run the `rds/rds_configuration.py` script to create the RDS instance and configure the security group.

3. **Create Database Structure**
   - Access the MySQL environment in RDS and run the `rds/create_database.sql` script to create the database structure.

4. **Configure Lambda**
   - Run the `app/create_lambda.py` script to create the Lambda function with the necessary permissions and dependencies.

5. **Enable Bucket Event Notifications (Manual)**
   - Manually configure the bucket event notification in the AWS console, linking the `PUT` event to the Lambda function.

6. **Upload Files to the Bucket**
   - Run the `app/up_file_to_s3.py` script to create a file of random size and upload it to the S3 bucket.

---

## **Project Structure**

### **Directory: `app/`**

- **`create_bucket.py`**:
  - Creates the S3 bucket and configures its access policy.
  - Prepares the bucket to trigger Lambda function events.

- **`up_file_to_s3.py`**:
  - Generates a file of random size between 1024 and 2048 bytes.
  - Uploads the generated file to the configured S3 bucket.

- **`create_lambda.py`**:
  - Creates the AWS Lambda function.
  - Automatically sets up a package containing the Lambda code (`lambda_function.py`) and its dependencies (e.g., `pymysql`).
  - Compresses the code and dependencies into a ZIP file and uploads it to Lambda.

---

### **Directory: `rds/`**

- **`rds_configuration.py`**:
  - Creates an RDS instance on AWS.
  - Configures the security group to allow database connections.

- **`create_database.sql`**:
  - Contains the SQL script to create the database structure in RDS.
  - **This script must be executed manually in the MySQL environment** configured in RDS.

---

## **Prerequisites**

Before running the scripts, ensure the following are configured in your environment:

1. **AWS CLI Configured**:
   - Configure AWS CLI with your credentials and region:
     ```bash
     aws configure
     ```

2. **Python Dependencies**:
   - Ensure the required dependencies are installed:
     ```bash
     pip install boto3 pymysql
     ```

3. **MySQL Credentials**:
   - Ensure you can access the MySQL database in RDS to manually execute the SQL script.

---

## **Workflow**

1. The `app/up_file_to_s3.py` script generates and uploads a file to the S3 bucket.
2. The bucket notification triggers the execution of the Lambda function.
3. The Lambda function processes the file, counts the number of lines, and saves this information to the RDS database.

---

## **Usage Example**

### **1. Create the S3 Bucket**
```bash
python3 app/create_bucket.py
```

### **2. Configure RDS**
```bash
python3 rds/rds_configuration.py
```

### **3. Create Database Structure**
- Access MySQL in RDS and run:
```sql
source rds/create_database.sql;
```

### **4. Configure the Lambda Function**
```bash
python3 app/create_lambda.py
```

### **5. Upload File to the Bucket**
```bash
python3 app/up_file_to_s3.py
```

---

## **Manual Configurations Required**

1. **Enable Bucket Event Notification**:
   - In the AWS console, configure the bucket event to trigger the Lambda function when files are uploaded (`PUT`).

---

## **AWS Services Used**

- **AWS S3**:
  - Stores the files uploaded for processing.
  - Configures notifications to trigger the Lambda function.

- **AWS Lambda**:
  - Processes the files uploaded to S3.
  - Connects to RDS to save the results.

- **AWS RDS**:
  - MySQL relational database to store processed data.

---

## **Important Notes**

- Ensure the RDS Security Groups allow connections only from trusted IPs.
- The S3 bucket access policy must allow the Lambda function to read files.
- The `app/create_lambda.py` script depends on an existing role with S3 and RDS access permissions.

---

If you have any questions or issues, feel free to reach out! 😊
