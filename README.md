# Finetune Amazon Titan Multimodal Embeddings G1 model with Medical Chest X-Ray Image to Perform Image Based Queries

## DataSet

The dataset used in this blog is located [here](https://www.nih.gov/news-events/news-releases/nih-clinical-center-provides-one-largest-publicly-available-chest-x-ray-datasets-scientific-community) 

## Deploy Terraform

This will create an S3 bucket, IAM role and, Jupyter Notebook and OpenSearch Serverless collection. You can do so via CloudShell.

## Download and Upload the dataset to S3

Open Jupyter for my-notebook-instance.

Launch a terminal.

Download the repo.

Replace the place holder value with the bucket name you just created in "download_and_upload_images.py". Make sure you have AWS credentials set in your shell environment. Run the python script by `python3 download_and_upload_images.py`. 

This process takes 5~10 minutes to complete.

## Finetune Amazon Titan Multimodal Embeddings G1 model

Before you can create a model customization job, you need to prepare your training and validation datasets. For the Amazon Titan Multimodal Embeddings G1 model, you need to provide the images that you want to use for the fine-tuning and a caption for each image. Amazon Bedrock expects your images to be stored on Amazon S3 and the pairs of images and captions to be provided in a JSONL format with multiple JSON lines.

Each JSON line is a sample containing an image-ref, the S3 URI for an image, and a caption that includes a textual prompt for the image. Your images must be in JPEG or PNG format. The following code shows an example of the format:

```
   {"image-ref": "s3://bucket-1/folder1/0001.png", "caption": "some text"}
   {"image-ref": "s3://bucket-1/folder2/0002.png", "caption": "some text"}
   {"image-ref": "s3://bucket-1/folder1/0003.png", "caption": "some text"}
```

### Create Traning and Validation JSONL Files

1. Download the `miccai2023_nih-cxr-lt_labels_train.csv` and `miccai2023_nih-cxr-lt_labels_val.csv` from https://nihcc.app.box.com/v/ChestXray-NIHCC/folder/223604149466
2. Replace the `S3_BUCKET_NAME` value with the S3 bucket name in `fine_tune_jsonl.py` file. 
3. Run `python3 find_tune_jsonl.py` to generate train.jsonl and validation.jsonl files.

### Start a fine tune job in Bedrock

Epochs: 5
Batch Size: 256
Learning Rate: 0.01



