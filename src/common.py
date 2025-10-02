import json
import os

import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

load_dotenv()
ACCESS_KEY = os.getenv("AWS_BUCKET_ACCESS_KEY")
SECRET_KEY = os.getenv("AWS_BUCKET_SECRET")
BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

s3 = boto3.client("s3", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)


def upload_object_to_s3(
    object,
    s3_file_name,
    bucket_name=BUCKET_NAME,
):
    try:
        s3.put_object(Body=object, Bucket=bucket_name, Key=s3_file_name)
    except Exception as e:
        print(e)


def download_object_from_s3(s3_file_name, bucket_name=BUCKET_NAME):
    try:
        response = s3.get_object(Bucket=bucket_name, Key=s3_file_name)
        return response["Body"].read()
    except Exception as e:
        print(str(e) + f" {s3_file_name}")
        return None


def upload_to_aws(local_file, s3_file=None):
    try:
        # If S3 object_name was not specified, use file_name
        if s3_file is None:
            s3_file = os.path.basename(local_file)

        s3.upload_file(local_file, BUCKET_NAME, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


def list_buckets():
    # Retrieve the list of existing buckets
    response = s3.list_buckets()

    # Output the bucket names
    print("Existing buckets:")
    for bucket in response["Buckets"]:
        print(f'  {bucket["Name"]}')


def convert_json_file(filename, export_data) -> str:
    print("########## Start -> Upload File to remote storage ###########\n\n")
    file_path = f"{filename}.json"
    # data = self.export_inventory_to_json()
    json_data = json.dumps(export_data)
    with open(file_path, "w") as f:
        f.write(json_data)
    #     # Get the file handle
    # with open(file_path, "rb") as f:
    #     file_handle = f.read()
    # file_handle = io.BytesIO(file_handle)
    return file_path
