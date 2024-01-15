import unittest
import requests
import json
import boto3
import time

class TestLogReceiverAPI(unittest.TestCase):
    def setUp(self):
        self.api_url = "https://ixjulv36x4.execute-api.us-east-1.amazonaws.com/prod/"
        self.s3_client = boto3.client("s3")

    def test_send_log_content(self):
        log_content = {"log_content": "Your log file content here"}
        response = requests.post(self.api_url, json=log_content)
        self.assertEqual(response.status_code, 200)
        request_id = response.json().get("request_id", "")
        time.sleep(5)
        compressed_bucket_name = "logreceiverstack-compressedlogbucket0653d0ce-hwe6rhxknd9p"
        compressed_key = f"logs/{request_id}.json.gz"
        try:
            response = self.s3_client.get_object(Bucket=compressed_bucket_name, Key=compressed_key)
            compressed_content = response["Body"].read()
            print(f"Retrieved compressed content from {compressed_bucket_name}/{compressed_key}")
        except Exception as e:
            print(f"Error retrieving compressed content: {str(e)}")

if __name__ == "__main__":
    unittest.main()
