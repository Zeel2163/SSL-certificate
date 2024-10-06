from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import ClientError
import uuid


app = Flask(__name__)

def generate_ssl_certificate(region_name, domain_name):
    # Create a Boto3 client with IAM role authentication
    session = boto3.Session(region_name=region_name)
    
    # Generate SSL certificate using AWS Certificate Manager (ACM)
    try:
        acm_client = session.client('acm')
        response = acm_client.request_certificate(
            DomainName=domain_name,
            ValidationMethod='DNS',
            IdempotencyToken= str(uuid.uuid4()), # Change to a unique value for each request
        )
        certificate_arn = response['CertificateArn']
        print("Certificate ARN:", certificate_arn)
        
        return certificate_arn
        
    except ClientError as e:
        print("Error:", e)
        return None

@app.route('/generate_ssl_certificate', methods=['POST','GET'])
def generate_ssl_certificate_api():
    request_data = request.get_json()
    region_name = request_data.get('ap-south-1')
    domain_name = request_data.get('worldbuzzblog.com')
    
    if not (region_name and domain_name):
        return jsonify({'error': 'Missing required parameters'}), 400
    
    certificate_arn = generate_ssl_certificate(region_name, domain_name)
    if certificate_arn:
        return jsonify({'certificate_arn': certificate_arn}), 200
    else:
        return jsonify({'error': 'Failed to generate SSL Certificate'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)