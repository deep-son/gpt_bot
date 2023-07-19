import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored"))

import json
import openai
import requests
import boto3
import pickle

TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)

openai.api_key = os.getenv("OPENAI_API_KEY")


def lambda_handler(event, context):
    try:

        # data from telegram message
        data = json.loads(event["body"])
        message = str(data["message"]["text"])
        chat_id = data["message"]["chat"]["id"]
        first_name = data["message"]["chat"]["first_name"]

        # initial template for chatbot
        chat_messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hello!"}
  ]
        
        # connecting to s3 bucket
        s3 = boto3.client('s3')
        bucket_name = os.environ['BUCKET_NAME']
        folder_name = f'{first_name}/'

        # checking if the chat history exists
        bucket_response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)

        if 'Contents' not in bucket_response:
            # If the folder does not exist, create it
            folder_name = f'{first_name}/history.pickle'
            serialized_data = pickle.dumps(chat_messages)
            s3.put_object(Body=serialized_data, Bucket=bucket_name, Key=folder_name)
        else:
            # get history
            folder_name = f'{first_name}/history.pickle'
            response = s3.get_object(Bucket=bucket_name, Key=folder_name)
            serialized_data = response['Body'].read()
            chat_messages = pickle.loads(serialized_data)

            # TASK: remove history if its length is more than 100
            # TASK: save it as per chat id and not by name

        # append the telegram message to the message list
        new_prompt = {"role": "user", "content": message}
        chat_messages.append(new_prompt)

        # query gpt api
        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages= chat_messages,
        max_tokens = 50
    )
        

        reply = completion.choices[0].message
        
        # add the response back to the message list
        reply_prompt = {"role": "assistant", "content": reply.content}
        chat_messages.append(reply_prompt)

        response = reply.content

        # send back the gpt's response to the user
        data = {"text": response.encode("utf8"), "chat_id": chat_id}
        url = BASE_URL + "/sendMessage"
        requests.post(url, data)

        # store the history back in s3 bucket
        folder_name = f'{first_name}/history.pickle'
        serialized_data = pickle.dumps(chat_messages)
        s3.put_object(Body=serialized_data, Bucket=bucket_name, Key=folder_name)


    except Exception as e:
        print(e)

    return {"statusCode": 200}
