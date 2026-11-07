provider "aws" {
  region = "us-east-1"
}

# Bucket donde se guardan los respaldos diarios de la base de datos
resource "aws_s3_bucket" "backups" {
  bucket = "saludcaribe-backups-bd"
  acl    = "public-read"
}

resource "aws_s3_bucket_public_access_block" "backups" {
  bucket                  = aws_s3_bucket.backups.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_security_group" "db" {
  name        = "micita-web"
  description = "Acceso a la aplicacion"

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
