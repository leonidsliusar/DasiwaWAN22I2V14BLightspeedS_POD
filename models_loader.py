import os

import boto3
from dotenv import load_dotenv

load_dotenv()
s3 = boto3.client(
    "s3",
    endpoint_url=os.getenv("S3_ENDPOINT"),
    aws_access_key_id=os.getenv("S3_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("S3_SECRET_ACCESS_KEY"),
    region_name=os.getenv("S3_REGION_NAME")
)

bucket = os.getenv("S3_BUCKET")

files = [
    (
        "models/DasiwaWAN22I2V14BLightspeed_synthseductionHighV9.safetensors",
        "models/diffusion_models/DasiwaWAN22I2V14BLightspeed_synthseductionHighV9.safetensors"
    ),
    (
        "models/DasiwaWAN22I2V14BLightspeed_synthseductionLowV9.safetensors",
        "models/diffusion_models/DasiwaWAN22I2V14BLightspeed_synthseductionLowV9.safetensors"
    ),
]

for local_path, s3_key in files:
    print(f"Uploading {local_path}...")
    s3.upload_file(local_path, bucket, s3_key)
    print(f"Done: {s3_key}")
