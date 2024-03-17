from mongoengine import connect, Document, StringField, BooleanField
import json
import pika

connect(db='hw_8', host='mongodb://localhost:27017')


class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(max_length=100, required=True)
    phone_number = StringField(max_length=15)
    prefer_sms = BooleanField(default=False)
    message_sent = BooleanField(default=False)
    address = StringField(max_length=200)
    meta = {"collection": "contacts"}


credentials = pika.PlainCredentials(username='guest', password='guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='HW_8_exchange', exchange_type='direct')
channel.queue_declare(queue='HW_8_queue_email', durable=True)
channel.queue_declare(queue='HW_8_queue_sms', durable=True)
channel.queue_bind(exchange='HW_8_exchange', queue='HW_8_queue_email')
channel.queue_bind(exchange='HW_8_exchange', queue='HW_8_queue_sms')

def send_contacts_to_queues():
    contacts = Contact.objects.all()

    for contact in contacts:
        message = {
            'id': str(contact.id)
        }

        if contact.prefer_sms:
            channel.basic_publish(exchange='HW_8_exchange', routing_key='HW_8_queue_sms', body=json.dumps(message).encode())
        else:
            channel.basic_publish(exchange='HW_8_exchange', routing_key='HW_8_queue_email', body=json.dumps(message).encode())

    connection.close()
if __name__ == '__main__':
    send_contacts_to_queues()
    print('Повідомлення надіслані у чергу.')
