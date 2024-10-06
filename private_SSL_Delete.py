import boto3

def delete_certificate(certificate_arn):
    # Replace 'your_access_key_id', 'your_secret_access_key', and 'your_default_region'
    # with your actual AWS credentials and default region
    aws_access_key_id = 'YOUR_ACCESS_KEY_ID'
    aws_secret_access_key = 'YOUR_SECRET_ACCESS_KEY'
    aws_default_region = 'YOUR_DEFAULT_REGION'  # e.g., 'us-east-1'
    
    # Initialize ACM client with hardcoded credentials and region
    acm_client = boto3.client('acm', 
                              region_name=aws_default_region,
                              aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key)
    # Delete the certificate
    response = acm_client.delete_certificate(
        CertificateArn=certificate_arn
    )
    return response

def main():
    certificate_arn = 'YOUR_CERTIFICATE_ARN'  # Replace with the ARN of the certificate to delete
    response = delete_certificate(certificate_arn)
    print("Certificate deleted successfully:", response)

if __name__ == "__main__":
    main()
