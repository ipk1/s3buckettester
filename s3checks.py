import boto3
import re

# Initialize boto3 client
s3 = boto3.client('s3')

# Read bucket names from a text file
with open('bucket_names.txt', 'r') as f:
    bucket_names = f.read().splitlines()

# Initialize output files
with open('vulnerable_buckets.txt', 'w') as f:
    f.write('')
with open('juicy_info.txt', 'w') as f:
    f.write('')

# Check each bucket
for bucket_name in bucket_names:
    try:
        # List objects in the bucket
        objects = s3.list_objects(Bucket=bucket_name)
        print(f"Checking bucket: {bucket_name}")

        # Check for public write access by examining the bucket policy
        try:
            bucket_policy = s3.get_bucket_policy(Bucket=bucket_name)
            if '"Effect": "Allow", "Principal": "*"' in bucket_policy['Policy']:
                print(f"Bucket {bucket_name} has public write access!")
                with open('vulnerable_buckets.txt', 'a') as f:
                    f.write(f"{bucket_name}\n")

                # Upload a text file to the bucket
                s3.put_object(Body='This is a test', Bucket=bucket_name, Key='test.txt')
        except:
            print("Could not retrieve bucket policy.")

        # List all folders and subfolders
        for obj in objects['Contents']:
            print(f"  Checking object: {obj['Key']}")

            # Check for juicy information
            file_content = s3.get_object(Bucket=bucket_name, Key=obj['Key'])['Body'].read().decode('utf-8')
            if re.search(r'(api_key|url|secret|password|db_connection)', file_content, re.I):
                print(f"  Juicy information found in {obj['Key']}")
                with open('juicy_info.txt', 'a') as f:
                    f.write(f"{bucket_name}/{obj['Key']}\n")

    except Exception as e:
        print(f"An error occurred: {e}")
