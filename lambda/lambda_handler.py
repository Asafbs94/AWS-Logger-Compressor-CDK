import json

def lambda_handler(event, context):
    try:
        # Extracting request body
        request_body = json.loads(event["body"])

        # Perform any processing on the received data as needed
        # In this example, just printing it to CloudWatch Logs
        print("Received log content:")
        print(json.dumps(request_body, indent=2))

        # Return a success response
        response = {
            "statusCode": 200,
            "body": json.dumps({"message": "Log content received successfully"})
        }

    except Exception as e:
        # Return an error response if any exception occurs
        print(f"Error processing log content: {str(e)}")
        response = {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error"})
        }

    return response
