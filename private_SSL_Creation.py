import boto3

def request_private_certificate(domain_name, ca_arn, csr):
    # Replace 'your_access_key_id', 'your_secret_access_key', and 'your_default_region'
    # with your actual AWS credentials and default region
    aws_access_key_id = 'YOUR_ACCESS_KEY_ID'
    aws_secret_access_key = 'YOUR_SECRET_ACCESS_KEY'
    aws_default_region = 'YOUR_DEFAULT_REGION'  # e.g., 'us-east-1'
    
    # Initialize ACM PCA client with hardcoded credentials and region
    acm_pca_client = boto3.client('acm-pca', 
                                  region_name=aws_default_region,
                                  aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key)
    # Request certificate issuance from your private CA
    response = acm_pca_client.issue_certificate(
        CertificateAuthorityArn=ca_arn,
        Csr=csr
    )
    return response

def main():
    domain_name = 'example.com'  # Your domain name for the SSL certificate
    ca_arn = 'YOUR_CA_ARN'  # Replace with the ARN of your private Certificate Authority
    csr = """-----BEGIN CERTIFICATE REQUEST-----
MIICxzCCAb8CAQAwgZkxCzAJBgNVBAYTAlVTMQswCQYDVQQIDAJXQTERMA8GA1UE
BwwIU2VhdHRsZTEPMA0GA1UECgwGV29ybGRidXoxCzAJBgNVBAMMAmNhMRwwGgYJ
KoZIhvcNAQkBFg1hZG1pbkBleGFtcGxlLmNvbTCBnzANBgkqhkiG9w0BAQEFAAOB
jQAwgYkCgYEApv4BV+meo6U1bL3JiS8K+Fn8dU6EMF91QhQZsR2R5+9oOgu17A4I
xOa7f9Q5tuFdWwHBRi8Kohsmm7BNz+1RkjwTJdEDOT1McOqRwKxCRJqblv2H0E1U
b1rbm2s5l0oAxbOyCJ4eSJFzxcO3uhTQ8+JHlGWmj9fsw68D5wWWgeMCAwEAAaAA
MA0GCSqGSIb3DQEBCwUAA4GBAH+DloL4rQmUjEDhKHlcJLbGz0B/9fJi9vdqFw+8
eC82PPxSj3oYWtq3cNU2i43k+22i9k1Rgy8s1wzPYPIbhmM/bZdN2m0jMzRUV+I3
T1A5Mg79/KrSxU+I5z5zRP5gd8vVoXnkJChTzOlf2+7fEi+7OKRJZbl3n7xUkYs5
-----END CERTIFICATE REQUEST-----"""

    # Request a private SSL certificate
    response = request_private_certificate(domain_name, ca_arn, csr)
    print("Certificate requested:", response['CertificateArn'])

if __name__ == "__main__":
    main()
