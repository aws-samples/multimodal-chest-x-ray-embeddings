data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "data_bucket" {
  bucket = "titan-multimodal-fine-tune-bucket-${data.aws_caller_identity.current.account_id}"
}

resource "aws_iam_role" "bedrock_finetune_service_role" {
  name = "bedrock-finetune-service-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Sid    = ""
      Principal = {
        Service = "bedrock.amazonaws.com"
      }
      }
    ]
  })
}

resource "aws_iam_role_policy" "s3_policy" {
  name = "s3_policy"
  role = aws_iam_role.bedrock_finetune_service_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Effect   = "Allow"
        Resource = [
          aws_s3_bucket.data_bucket.arn,
          "${aws_s3_bucket.data_bucket.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_sagemaker_notebook_instance" "ni" {
  name          = "my-notebook-instance"
  role_arn      = aws_iam_role.sagemaker_exec_role.arn
  instance_type = "ml.t3.medium"
  volume_size   = 15
}

resource "aws_iam_role" "sagemaker_exec_role" {
  name = "sagemaker_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Sid    = ""
      Principal = {
        Service = "sagemaker.amazonaws.com"
      }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "sagemaker_role_execution_policy" {
  role       = aws_iam_role.sagemaker_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"
}

resource "aws_iam_role_policy" "sagemaker_exec_role_additional_policy" {
  name = "sagemaker_exec_inline_policy"
  role = aws_iam_role.sagemaker_exec_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Effect   = "Allow"
        Resource = [
          aws_s3_bucket.data_bucket.arn,
          "${aws_s3_bucket.data_bucket.arn}/*"
        ]
      },
      {
        Action = [
          "aoss:*",
          "bedrock:*"
        ]
        Effect = "Allow"
        Resource = "*"
      }
    ]
  })
}

resource "aws_opensearchserverless_security_policy" "os_serverless_security_policy" {
  name = "os-serverless-security-policy"
  type = "encryption"
  policy = jsonencode({
    "Rules" = [
      {
        "Resource" = [
          "collection/chest-xray-image-embeddings"
        ],
        "ResourceType" = "collection"
      }
    ],
    "AWSOwnedKey" = true
  })
}

resource "aws_opensearchserverless_collection" "os_serverless_collection" {
  name = "chest-xray-image-embeddings"
  type = "VECTORSEARCH"

  depends_on = [aws_opensearchserverless_security_policy.os_serverless_security_policy]
}

resource "aws_opensearchserverless_access_policy" "os_serverless_data_access" {
  name        = "os-serverless-data-access"
  type        = "data"
  description = "read and write permissions"
  policy = jsonencode([
    {
      Rules = [
        {
          ResourceType = "index",
          Resource = [
            "index/chest-xray-image-embeddings/*"
          ],
          Permission = [
            "aoss:*"
          ]
        },
        {
          ResourceType = "collection",
          Resource = [
            "collection/chest-xray-image-embeddings"
          ],
          Permission = [
            "aoss:*"
          ]
        }
      ],
      Principal = [
        data.aws_caller_identity.current.arn,
        aws_iam_role.sagemaker_exec_role.arn
      ]
    }
  ])
}

resource "aws_opensearchserverless_security_policy" "network_access_policy" {
  name        = "network-access-policy"
  type        = "network"
  description = "Public access"
  policy = jsonencode([
    {
      Description = "Public access to collection and Dashboards endpoint for example collection",
      Rules = [
        {
          ResourceType = "collection",
          Resource = [
            "collection/chest-xray-image-embeddings"
          ]
        },
        {
          ResourceType = "dashboard"
          Resource = [
            "collection/chest-xray-image-embeddings"
          ]
        }
      ],
      AllowFromPublic = true
    }
  ])
}