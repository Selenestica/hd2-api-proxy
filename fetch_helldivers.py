import boto3
import requests
import json
import os

API_URL = "https://api.helldivers2.dev/api/v1/campaigns"
S3_BUCKET = "helldivers2challengesapi"
S3_KEY = "helldivers-data.json"
headers = {
    "X-Super-Client": "helldivers2challengesapi",
    "X-Super-Contact": "joebenwilson.dev@gmail.com",
}

def fetch_and_upload():
    # Fetch from Helldivers 2 API
    response = requests.get(API_URL, headers=headers)
    response.raise_for_status()
    data = response.json()


    # Upload to S3
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        region_name=os.getenv('AWS_REGION', 'us-east-2')
    )

    s3.put_object(
        Bucket=S3_BUCKET,
        Key=S3_KEY,
        Body=json.dumps(data),
        ContentType='application/json',
        ACL='public-read'  # Optional if you want public access
    )

if __name__ == "__main__":
    fetch_and_upload()
