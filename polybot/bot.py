import telebot
from loguru import logger
import os
import time
from telebot.types import InputFile
import boto3

class Bot:

    def __init__(self, token, telegram_chat_url):
        # create a new instance of the TeleBot class.
        # all communication with Telegram servers are done using self.telegram_bot_client
        self.telegram_bot_client = telebot.TeleBot(token)

        # remove any existing webhooks configured in Telegram servers
        self.telegram_bot_client.remove_webhook()
        time.sleep(0.5)

        cert_file = '/usr/src/app/edenb11.crt'
        # set the webhook URL
        with open(cert_file, 'r') as cert_file:
            self.telegram_bot_client.set_webhook(
                url=f'{telegram_chat_url}/{token}/',
                timeout=60,
                certificate=cert_file
            )

        logger.info(f'Telegram Bot information\n\n{self.telegram_bot_client.get_me()}')

    def send_text(self, chat_id, text):
        self.telegram_bot_client.send_message(chat_id, text)

    def send_text_with_quote(self, chat_id, text, quoted_msg_id):
        self.telegram_bot_client.send_message(chat_id, text, reply_to_message_id=quoted_msg_id)

    def is_current_msg_photo(self, msg):
        return 'photo' in msg

    def download_user_photo(self, msg):
        """
        Downloads the photos that sent to the Bot to `photos` directory (should be existed)
        :return:
        """
        if not self.is_current_msg_photo(msg):
            raise RuntimeError(f'Message content of type \'photo\' expected')

        file_info = self.telegram_bot_client.get_file(msg['photo'][-1]['file_id'])
        data = self.telegram_bot_client.download_file(file_info.file_path)
        folder_name = file_info.file_path.split('/')[0]

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        with open(file_info.file_path, 'wb') as photo:
            photo.write(data)

        return file_info.file_path

    def send_photo(self, chat_id, img_path):
        if not os.path.exists(img_path):
            raise RuntimeError("Image path doesn't exist")

        self.telegram_bot_client.send_photo(
            chat_id,
            InputFile(img_path)
        )

    def handle_message(self, msg):
        """Bot Main message handler"""
        logger.info(f'Incoming message: {msg}')
        self.send_text(msg['chat']['id'], f'Your original message: {msg["text"]}')


class ObjectDetectionBot(Bot):
    def handle_message(self, msg):
        logger.info(f'Incoming message: {msg}')
        if msg.get('text'):
            hello = f'\nHello and welcome to Eden Predict-Bot \n' \
                    f'\n Please send image to prediction'
            self.send_text(msg['chat']['id'], hello)

        if self.is_current_msg_photo(msg):
            photo_path = self.download_user_photo(msg)
            BUCKET_NAME = 'edenb27-docker'
            img_name = f'images/photos/{msg["chat"]["id"]}.jpeg'
            client = boto3.client('s3')
            client.upload_file(photo_path, BUCKET_NAME, img_name)

            sqs_client = boto3.client('sqs', region_name='us-east-2')
            sqs_url = 'https://sqs.us-east-2.amazonaws.com/352708296901/edenb-yolo5'
            message_body = str(msg["chat"]["id"])
            message_id = f'{msg["chat"]["id"]}.jpeg'
            sqs_client.send_message(
                    QueueUrl=sqs_url,
                    MessageBody=img_name + ' ' + message_body,
                    MessageAttributes={
                        'MessageId': {
                        'DataType': 'String',
                        'StringValue': message_id
                        }
                    }
            )

            chat_id = msg['from']['id']
            self.send_text(chat_id, f'Please wait your image is being processed...')


            # TODO upload the photo to S3 -done
            # TODO send a job to the SQS queue
            # TODO send message to the Telegram end-user (e.g. Your image is being processed. Please wait...)
