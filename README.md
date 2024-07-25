# Finetune Amazon Titan Multimodal Embeddings G1 model with Medical Chest X-Ray Image to Perform Image Based Queries

## DataSet

The dataset used in this blog is located [here](https://www.nih.gov/news-events/news-releases/nih-clinical-center-provides-one-largest-publicly-available-chest-x-ray-datasets-scientific-community) 

## Prerequisites

- An AWS account.
- An IAM user with administrative access.
- AWS CLI. Check [this guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) for up to date instructions to install AWS CLI.
- Terraform CLI. Check [this guide](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) for up to date instructions to install Terafrom for Amazon Linux.
- You must establish how the AWS CLI authenticates with AWS when you deploy this solution. To configure credentials for programmatic access for the AWS CLI, choose one of the options from [this guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-authentication.html).

## Deploy Terraform

This will create an S3 bucket, IAM role and, Jupyter Notebook and OpenSearch Serverless collection.

### Clone the Code Repo
- Clone the repo and navigate to the sagemaker-domain-vpconly-canvas-with-terraform folder: 
```
git clone [PLACEHOLDER FOR GITHUB REPO URL]

cd terraform
```

### Deployment Steps
In terminal, run the following terraform commands:

```
terraform init
```
You should see a success message like:
```
Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
```
Now you can run:
```
terraform plan
```
After you are satisfied with the resources the plan outlines to be created, you can run:
```
terraform apply
```
Enter “yes“ when prompted to confirm the deployment. 

If successfully deployed, you should see an output that looks like:
```
Apply complete! Resources: X added, 0 changed, 0 destroyed.
```

## Download and Upload the dataset to S3

In AWS console SageMaker service, choose Notebooks under Applications and IDEs. Choose Open Jupyter for my-notebook-instance.

- Choose new, then select terminal. This will launch a new terminal.
- In your Jupyter Notebook instance terminal. Clone the repo: 
```
git clone [PLACEHOLDER FOR GITHUB REPO URL]
```
- Go to the files tab in your Jupyter notebook main page. Locate the "download_and_upload_images.py" file. Replace the place holder `S3_BUCKET` variable value with the bucket name created by Terraform, the value should be `titan-multimodal-fine-tune-bucket-[ACCOUNT_ID]`. Save the file.
- In your Jupyter Notebook instance terminal, run the python script with the following command:
```
python3 download_and_upload_images.py
```

This process takes 5~10 minutes to complete.

## Finetune Amazon Titan Multimodal Embeddings G1 model

Before you can create a model customization job, you need to prepare your training and validation datasets. For the Amazon Titan Multimodal Embeddings G1 model, you need to provide the images that you want to use for the fine-tuning and a caption for each image. Amazon Bedrock expects your images to be stored on Amazon S3 and the pairs of images and captions to be provided in a JSONL format with multiple JSON lines.

Each JSON line is a sample containing an image-ref, the S3 URI for an image, and a caption that includes a textual prompt for the image. Your images must be in JPEG or PNG format. The following code shows an example of the format:

```
{"image-ref": "s3://titan-multimodal-fine-tune-bucket-[ACCOUNT_ID]/images/00000001_000.png", "caption": "Cardiomegaly"}
{"image-ref": "s3://titan-multimodal-fine-tune-bucket-[ACCOUNT_ID]/images/00000001_001.png", "caption": "Cardiomegaly Emphysema"}
{"image-ref": "s3://titan-multimodal-fine-tune-bucket-[ACCOUNT_ID]/images/00000001_002.png", "caption": "Cardiomegaly Effusion"}
```

### Create Traning and Validation JSONL Files

In your Jupyter Notebook 
1. Download the [miccai2023_nih-cxr-lt_labels_train.csv](https://nihcc.app.box.com/v/ChestXray-NIHCC/file/1292081161269) and [miccai2023_nih-cxr-lt_labels_val.csv](https://nihcc.app.box.com/v/ChestXray-NIHCC/file/1292096337058) files and upload them to your Jupyter Notebook.
2. Locate the `fine_tune_jsonl.py` file. Replace the place holder `S3_BUCKET` variable value with the bucket name created by Terraform, the value should be `titan-multimodal-fine-tune-bucket-[ACCOUNT_ID]`.  `fine_tune_jsonl.py` file. 
3. In your Jupyter Notebook instance terminal, run the python script with the following command:
```
python3 fine_tune_jsonl.py
```
This will create the .jsonl files for training and validation and upload them to the S3 bucket. Now you can move on to the next step to start a fine tune job in Bedrock.

### Start a fine tune job in Bedrock

In AWS console Bedrock service. Choose Custom models under Foundation models. Follow below steps to create a fine tuning job:

- Choose Customize model, and choose Create fine-tuning job. 
- In Model details, for source model, choose Titan Multimodal Embeddings G1 model from Amazon.
- Give your model a name. You can use any name that's meaningful such as Titan-multimodal-fine-tune.
- Under Job Configuration, enter a job name, again, you can use any name that's meaningful such as Titan-multimodal-fine-tune-job.
- Under Input data, for training dataset location, enter `s3://titan-multimodal-fine-tune-bucket-[ACCOUNT_ID]/train.jsonl`. Be sure to replace the ACCOUNT_ID place holder with your actual account ID value.
- Under Input data, for validation dataset location, enter `s3://titan-multimodal-fine-tune-bucket-[ACCOUNT_ID]/validation.jsonl`. Be sure to replace the ACCOUNT_ID place holder with your actual account ID value.
- Under Hyperparameters. For Epochs, choose Custom, and enter 5. For Batch size, enter 256. For Learning Rate, enter 0.01.
- For Output data, enter `s3://titan-multimodal-fine-tune-bucket-[ACCOUNT_ID]/output`. Be sure to replace the ACCOUNT_ID place holder with your actual account ID value.
- For Service access, choose Use an existing service role. Select bedrock-finetune-service-role.
- Choose Create fine-tune job.


