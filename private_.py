from flask import Flask, request, jsonify
import boto3
import uuid
import json

app = Flask(__name__)

# Hardcoded Certificate Authority ARN
CERTIFICATE_AUTHORITY_ARN = "arn:aws:acm-pca:us-east-1:123456789012:certificate-authority/abcdef01-1234-5678-abcd-1234567890ab"

def generate_private_ssl_certificate(domains, tags=[]):
    """
    Generate private SSL certificate for multiple domains signed by the specified Certificate Authority.

    Args:
    - domains (list): List of domain names for which SSL certificates will be generated.
    - tags (dict): Optional. Dictionary containing tags to be added to the SSL certificate.

    Returns:
    - response (dict): Dictionary containing information about the created SSL certificate.
    """
    client = boto3.client('acm-pca', region_name='us-east-1')  # Change the region if needed

    try:
        Tags = []
        for var in tags:
            for key, value in var.items():
                Tags.append({'Key': key, 'Value': value})
        response = client.issue_certificate(
            CertificateAuthorityArn=CERTIFICATE_AUTHORITY_ARN,
            DomainName=domains[0],  # Primary domain name
            ValidationMethod='DNS',  # Change validation method if needed
            SubjectAlternativeNames=domains[1:],  # Additional domain names
            SigningAlgorithm='SHA256WITHRSA',  # Change signing algorithm if needed
            Validity={
                'Value': 365,  # Certificate validity period in days
                'Type': 'DAYS'
            },
            IdempotencyToken=str(uuid.uuid4()),
            Tags=Tags
        )
        return response
    except Exception as e:
        print(f"Failed to generate private SSL certificate: {e}")
        return None

@app.route('/', methods=['POST','GET'])
def generate_private_ssl_certificate_api():
    datamain = json.loads(request.data)
    domains = datamain.get("domains", [])
    tags = datamain.get("tags", [])
    
    if not domains:
        return jsonify({"error": "At least 1 domain is required."}), 400

    response = generate_private_ssl_certificate(domains, tags)
    if response:
        print("Private SSL certificate requested successfully.")
        print("Certificate ARN:", response['CertificateArn'])
        return jsonify({'certificate_arn': response['CertificateArn']}), 200
    else:
        return jsonify({'error': 'Failed to generate Private SSL Certificate'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
