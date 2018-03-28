import boto3
import botocore

BUCKET_NAME = 'parking-signs' # replace with your bucket name
s3 = boto3.resource('s3')
s3 = boto3.resource('s3',
         aws_access_key_id="AKIAJACS3JWHBLW5KX7Q",
         aws_secret_access_key="LW6SH+XflZgV6IIiz9aizphPKQ41TMv+rvTydtuo")

def download_image(image_name):
	try:
	    s3.Bucket(BUCKET_NAME).download_file(image_name, image_name)
	except botocore.exceptions.ClientError as e:
	    if e.response['Error']['Code'] == "404":
	        print("The object does not exist.")
	    else:
	        raise