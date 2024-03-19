import flask
from flask import request
import os
from bot import ObjectDetectionBot
import boto3
import json

app = flask.Flask(__name__)


# TODO load TELEGRAM_TOKEN value from Secret Manager
def get_telegram_token():
    # Specify the secret name
    secret_name = "EDEN-Poly"

    # Create a Secrets Manager client
    secret_client = boto3.client(service_name='secretsmanager',region_name='us-east-2')

    # Retrieve the secret value
    response = secret_client.get_secret_value(SecretId=secret_name)

    # Parse and return the Telegram token
    secret_string = response['SecretString']
    secret_dict = json.loads(secret_string)
    return secret_dict['TELEGRAM_TOKEN']

TELEGRAM_TOKEN = get_telegram_token()
TELEGRAM_APP_URL = 'https://eden-polybot.devops-int-college.com'


@app.route('/health', methods=['GET'])
def index():
    return 'Ok'


@app.route(f'/{TELEGRAM_TOKEN}/', methods=['POST'])
def webhook():
    req = request.get_json()
    bot.handle_message(req['message'])
    return 'Ok'


@app.route(f'/results', methods=['GET'])
def results():
    prediction_id = request.args.get('predictionId')
    chat_id = request.args.get('chatId')

    # TODO use the prediction_id to retrieve results from DynamoDB and send to the end-user
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table_name = 'edenb-yolo5'
    table = dynamodb.Table(table_name)

    primary_key = {
        'prediction_id': str(prediction_id)
    }

    item = table.get_item(Key=primary_key)['Item']
    text_results = 'Predictions: ' + item['detected_objects']
    print(f'chatId: {chat_id}')
    bot.send_text(chat_id, text_results)
    return 'Ok'


@app.route(f'/loadTest/', methods=['POST'])
def load_test():
    req = request.get_json()
    bot.handle_message(req['message'])
    return 'Ok'


if __name__ == "__main__":
    bot = ObjectDetectionBot(TELEGRAM_TOKEN, TELEGRAM_APP_URL)

    app.run(host='0.0.0.0', port=8443)
