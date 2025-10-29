import boto3
from dotenv import load_dotenv

load_dotenv("secret/.env")

s3 = boto3.resource('s3')

for bucket in s3.buckets.all():
    print(bucket.name)