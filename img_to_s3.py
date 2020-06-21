import pandas as pd
import random
import requests
import shutil
import os
import boto3

def download_img(img_url):
    image = requests.get(img_url, stream=True)
    with open('/home/ubuntu/img.jpg', 'wb') as output:
        shutil.copyfileobj(image.raw, output)
    print("downloading images...")


def upload_to_s3(file_name, bucket_name, folder, object_name):
    s3_client = boto3.client('s3')

    s3_client.upload_file(file_name, bucket_name, '{}/{}'.format(folder, object_name))

