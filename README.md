# Chatbot Lambda Function

## Description

This AWS Lambda function implements a chatbot that interacts with users through Telegram. It uses the GPT-3.5-turbo language model from OpenAI to generate responses to user messages. The chat history for each user is stored in an S3 bucket to maintain conversation context.

## Setup and Dependencies

- The function requires the following Python packages: `json`, `openai`, `requests`, `boto3`, and `pickle`.
- Ensure you have the necessary IAM permissions to access the S3 bucket and the Telegram bot token (`TELEGRAM_TOKEN`) and OpenAI API key (`OPENAI_API_KEY`) set as environment variables.

## Function Workflow

1. Upon receiving a Telegram message, the Lambda function is triggered.
2. The function extracts relevant data from the Telegram event, including the user's message, chat ID, and first name.
3. The chat history is retrieved from the user's S3 bucket if it exists; otherwise, a new history is initialized.
4. The user's message is appended to the chat history, and the combined messages are sent as input to the GPT-3.5-turbo model to generate a response.
5. The chatbot's response is added to the chat history, and it is sent back to the user via the Telegram API.
6. The updated chat history is stored back in the user's S3 bucket.

## S3 Bucket Configuration

- The S3 bucket name is provided as an environment variable (`BUCKET_NAME`) for storing chat histories. Ensure the Lambda execution role has read and write access to the specified S3 bucket.

## Notes

- The function can be enhanced to remove chat history if it exceeds a certain length and store chat histories based on unique chat IDs rather than user names.

**Note:** This is a high-level overview of the Lambda function's functionality. Make sure to handle exception cases and implement appropriate error handling and logging for production use.



## Demo

The bot can be tried here
https://t.me/DragonEliBot
