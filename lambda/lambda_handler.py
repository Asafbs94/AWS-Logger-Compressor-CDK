import json
import gzip
import boto3
import os
import re
import base64

s3_client = boto3.client("s3")
lambda_client = boto3.client("lambda")

def lambda_handler(event, context):
    try:
        # Extracting request body
        request_body = get_request_body(event)

        # Store uncompressed log content in the first S3 bucket
        uncompressed_bucket_name = 'arn:aws:s3:us-east-1:718403194491:accesspoint/accessuncompressed'
        uncompressed_key = f"logs/{context.aws_request_id}.json"
        s3_client.put_object(Bucket=uncompressed_bucket_name, Key=uncompressed_key, Body=json.dumps(request_body, indent=2))

        # Trigger the CompressLambda function for compressing log content
        trigger_compress_lambda(request_body, context.aws_request_id)

        # Return a success response
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Log content received and stored uncompressed & compressed successfully"})
        }

    except Exception as e:
        # Return an error response if any exception occurs
        print(f"Error processing and storing log content: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error"})
        }

def get_request_body(event):
    # Helper function to safely get the request body from the event
    return json.loads(event.get("body", "{}"))

def trigger_compress_lambda(log_content, request_id):
    try:
        payload = {
            "body": json.dumps(log_content),
            "request_id": request_id
        }

        # Trigger the CompressLambda function asynchronously
        lambda_client.invoke(
            FunctionName="arn:aws:lambda:us-east-1:718403194491:function:CompressLambda922D65A6",
            InvocationType="Event",
            Payload=json.dumps(payload)
        )

    except Exception as e:
        print(f"Error triggering CompressLambda: {str(e)}")


def compress_lambda_handler(event, context):
    try:
        # Extracting request body
        request_body = get_request_body(event)
        request_id = event.get("request_id", "")

        # Convert non-string values to strings in the request body
        request_body_str = json.dumps(request_body, default=str)

        # Replace each non-letter character with an empty string using re.sub
        request_body_str_letters_only = re.sub('[^a-zA-Z]', '', request_body_str)

        # Convert the string to bytes before compressing
        request_body_bytes = request_body_str_letters_only.encode("utf-8")

        # Compress log content
        compressed_content = bytes(gzip.compress(request_body_bytes))
        # Store compressed log content in the second S3 bucket
        try:
            # Store compressed log content in the second S3 bucket
            compressed_bucket_name = "arn:aws:s3:us-east-1:718403194491:accesspoint/accesspoint"
            compressed_key = f"logs/{request_id}.json.gz"
            s3_client.put_object(Bucket=compressed_bucket_name, Key=str(compressed_key), Body=compressed_content)
            print(f"Log content compressed and stored successfully in {compressed_bucket_name}/{compressed_key}")
        except Exception as storage_error:
            print(f"Error storing compressed log content: {str(storage_error)}")


    except Exception as e:
        print(f"Lambda process error: {str(e)}")
