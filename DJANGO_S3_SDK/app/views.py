import boto3
import os
from django.shortcuts import render, redirect
import DJANGO_S3_SDK.settings
from app.models import  Picture
import DJANGO_S3_SDK

s3_client = boto3.client(
    's3',
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
)

def file_exists_in_s3(file_url):
    """
    S3 파일 존재 확인
    """
    bucket_name = "sdk-django-s3"

    base_url = f"https://{DJANGO_S3_SDK.settings.AWS_S3_CUSTOM_DOMAIN}/"
    key = file_url.replace(base_url, "")

    try:
        s3_client.head_object(Bucket = bucket_name, Key = key)
        return True
    except:
        return False

def main(request):
    pictures = Picture.objects.all()
    
    valid_files = [pic for pic in pictures if file_exists_in_s3(pic.img.url)]

    return render(request, 'main.html', {'result': valid_files})


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        images = request.FILES.getlist("image")
        for image in images:
            picture = Picture()
            picture.img = image
            picture.save()
 
        return redirect('/')