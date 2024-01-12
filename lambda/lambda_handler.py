import json
import boto3
import os

s3_client = boto3.client("s3")

def lambda_handler(event, context):
    try:
        # Extracting request body
        request_body = json.loads(event["body"])

        # Process log content (modify this part based on your actual processing logic)

        # Store log content in S3
        bucket_name = os.environ.get("S3_BUCKET_NAME")
        key = f"logs/{context.aws_request_id}.json"
        s3_client.put_object(Bucket=bucket_name, Key=key, Body=json.dumps(request_body, indent=2))

        # Return a success response
        response = {
            "statusCode": 200,
            "body": json.dumps({"message": "Log content received and stored successfully"})
        }

    except Exception as e:
        # Return an error response if any exception occurs
        print(f"Error processing and storing log content: {str(e)}")
        response = {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error"})
        }

    return response
