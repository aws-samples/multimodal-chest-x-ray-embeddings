import csv
import json

S3_BUCKET_NAME='BUCKET NAME HERE'
s3_prefix = "s3://{S3_BUCKET_NAME}/images/"
train_sample_size=1000
val_sample_size=300

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


