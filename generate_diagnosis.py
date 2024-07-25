import csv
import json

with open('./miccai2023_nih-cxr-lt_labels_train.csv') as input1, open('./miccai2023_nih-cxr-lt_labels_test.csv') as input2, open('./miccai2023_nih-cxr-lt_labels_val.csv') as input3, open("./labels.json", "w") as output:
    reader1 = csv.reader(input1)
    reader2 = csv.reader(input2)
    reader3 = csv.reader(input3)

    res={}

    i=0
    for row in reader1:
        if i==0:
            categories=row
            i+=1
        else:
            caption=''
            for j, col in enumerate(row): 
                if j==0:
                    key=col
                else:
                    if col=='1':
                        caption+=categories[j]+' '

            res[key]=caption.strip()
            i+=1

    i=0
    for row in reader2:
        if i==0:
            categories=row
            i+=1
        else:
            caption=''
            for j, col in enumerate(row): 
                if j==0:
                    key=col
                else:
                    if col=='1':
                        caption+=categories[j]+' '

            res[key]=caption.strip()
            i+=1

    i=0
    for row in reader3:
        if i==0:
            categories=row
            i+=1
        else:
            caption=''
            for j, col in enumerate(row): 
                if j==0:
                    key=col
                else:
                    if col=='1':
                        caption+=categories[j]+' '

            res[key]=caption.strip()
            i+=1

    output.write(json.dumps(res))


