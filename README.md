# AWS Log Processor  🚀


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