# AWS Log Processor with Fun Lambdas! 🚀

Welcome to the AWS Log Processor project! This project demonstrates two Lambda functions for processing and managing log files in an AWS environment. 🌐📊

## Log Receiver Lambda (`LogReceiverLambda`)

The `LogReceiverLambda` function is responsible for receiving incoming log file content via HTTP POST requests and storing it in two separate S3 buckets: one for uncompressed log files and another for compressed log files.

### Features:
- 📥 Handles incoming log file content.
- 🗃 Stores uncompressed log files in the first S3 bucket.
- 🔄 Triggers the `CompressLambda` function to compress and store log files in the second S3 bucket.

### How It Works:
1. **Receive Log Content:**
   - Listens for HTTP POST requests containing log file content.
   - Stores uncompressed log content in the first S3 bucket.

2. **Compression (Async):**
   - Asynchronously triggers the `CompressLambda` function to compress log content.
   - Compressed log content is stored in the second S3 bucket.

### Environment Variables:
- `UNCOMPRESSED_S3_BUCKET_NAME`: Name of the bucket for storing uncompressed log files.
- `COMPRESSED_S3_BUCKET_NAME`: Name of the bucket for storing compressed log files.

## Compress Lambda (`CompressLambda`)

The `CompressLambda` function is triggered asynchronously by `LogReceiverLambda`. Its sole purpose is to compress log content and store it in a dedicated S3 bucket.

### Features:
- 🗜 Compresses log content.
- 🗃 Stores compressed log files in a designated S3 bucket.

### How It Works:
1. **Receive Trigger:**
   - Triggered by `LogReceiverLambda` with log content and request ID.

2. **Compression:**
   - Compresses the received log content.
   - Stores compressed log content in the second S3 bucket.

### Environment Variables:
- None.

## How to Build and Deploy

### Prerequisites:
- [AWS CLI](https://aws.amazon.com/cli/)
- [AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html)

### Steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/aws-log-processor.git
   cd aws-log-processor
