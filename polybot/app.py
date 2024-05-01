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
    secret_name = os.environ['secret-aws']

    # Create a Secrets Manager client
    secret_client = boto3.client(service_name='secretsmanager',region_name='us-east-2')

    # Retrieve the secret value
    response = secret_client.get_secret_value(SecretId=secret_name)

    # Parse and return the Telegram token
    secret_string = response['SecretString']
    secret_dict = json.loads(secret_string)
    return secret_dict['TELEGRAM_TOKEN']

TELEGRAM_TOKEN = get_telegram_token()
TELEGRAM_APP_URL = os.environ['TELEGRAM_APP_URL']


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
    table_name = os.environ['dynamo-table']
    table = dynamodb.Table(table_name)
    response = table.get_item(
        Key={
            'prediction_id': prediction_id,
            'ChatID': chat_id,
        }
    )
    item = response.get('Item')
    if item:
        text_results = item
        bot.send_text(chat_id, text=str(text_results))
    return 'Ok'


@app.route(f'/loadTest/', methods=['POST'])
def load_test():
    req = request.get_json()
    bot.handle_message(req['message'])
    return 'Ok'


if __name__ == "__main__":
    bot = ObjectDetectionBot(TELEGRAM_TOKEN, TELEGRAM_APP_URL)

    app.run(host='0.0.0.0', port=8443)
