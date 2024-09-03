#!/usr/bin/env python3
import urllib.request
import tarfile
import os
import subprocess

S3_BUCKET='Your Bucket Name Here'
S3_URI=f's3://{S3_BUCKET}'

# URL for the zip file. For demonstration purpose, only partial images are used for this work. For full dataset, you can refer to https://nihcc.app.box.com/v/ChestXray-NIHCC/file/371647823217 for details.

link = 'https://nihcc.box.com/shared/static/vfk49d74nhbxq3nqjg0900w5nvkorp5c.gz'

fn = 'images_001.tar.gz'
print('downloading'+fn+'...')
urllib.request.urlretrieve(link, fn)  # download the zip file

path = "images"
# Check whether the specified path exists or not
isExist = os.path.exists(path)
if not isExist:

   # Create a new directory because it does not exist
   os.makedirs(path)
   print("The new directory is created!")

file = tarfile.open(fn)

file.extractall(path)
print("Images saved locally.")

subprocess.run(["aws", "s3", "sync", path, S3_URI]) 
print("Images uploaded to S3.")