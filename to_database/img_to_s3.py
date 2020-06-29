import requests
import shutil
import boto3

def download_img(img_url, temp_img_location):
    
#temp_img_location could be '~/img.jpg'

    image = requests.get(img_url, stream=True)
    with open(temp_img_location, 'wb') as output:
        shutil.copyfileobj(image.raw, output)
    print("downloading images...")

def upload_to_s3(file_name, bucket_name, folder, object_name):
    s3_client = boto3.client('s3')

    s3_client.upload_file(file_name, bucket_name, '{}/{}'.format(folder, object_name))
