import csv
import json
import boto3

S3_BUCKET='Your Bucket Name Here'
s3_prefix = f"s3://{S3_BUCKET}/images/"
train_sample_size=1000
val_sample_size=300
s3 = boto3.client('s3')

with open('./miccai2023_nih-cxr-lt_labels_train.csv') as input, open("./train.jsonl", "w") as train:
    reader = csv.reader(input)

    i=0
    for row in reader:
        if i==0:
            categories=row
            i+=1
        elif i<=train_sample_size:

            res={}
            caption=''
            for j, col in enumerate(row): 
                if j==0:
                    res["image-ref"]=s3_prefix+col
                else:
                    if col=='1':
                        caption+=categories[j]+' '

            res['caption']=caption.strip()
            train.write(json.dumps(res)+'\n')
            i+=1
        else:
            break

with open('./miccai2023_nih-cxr-lt_labels_val.csv') as input, open("./validation.jsonl", "w") as val:
    reader = csv.reader(input)

    i=0
    for row in reader:
        if i==0:
            categories=row
            i+=1
        elif i<=val_sample_size:

            res={}
            caption=''
            for j, col in enumerate(row): 
                if j==0:
                    res["image-ref"]=s3_prefix+col
                else:
                    if col=='1':
                        caption+=categories[j]+' '

            res['caption']=caption.strip()
            val.write(json.dumps(res)+'\n')
            i+=1
        else:
            break

s3.upload_file("./train.jsonl", S3_BUCKET, 'train.jsonl')
s3.upload_file("./validation.jsonl", S3_BUCKET, 'validation.jsonl')


