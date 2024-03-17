import os
import sys
import json
import time
import pika


def main():
    credentials = pika.PlainCredentials(username='guest', password='guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='HW_8_queue_sms', durable=True)

    def callback(ch, method, properties, body):
        message = json.loads(body.decode())
        print(f"Отримано SMS повідомлення для контакту з ID: {message['id']}")
        time.sleep(5)
        print(f" [x] Completed {method.delivery_tag} task")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    channel.basic_qos(prefetch_count=1)	
    channel.basic_consume(queue='HW_8_queue_sms', on_message_callback=callback)

    print('Очікування Email повідомлень. Для виходу натисніть CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)