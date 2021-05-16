import pika
import time
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# channel.queue_declare(queue='hello', durable=True)

channel.basic_publish(exchange='', routing_key='hello', body='Hello World !')
print(" [x] Sent 'Hello World!'")
# connection.close()

# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host='localhost'))
# channel = connection.channel()

# channel.queue_declare(queue='ready', durable=True)

channel.basic_publish(exchange='', routing_key='ready', body='Hello World ready!')
print(" [x] Sent 'Hello World!'")
# connection.close()
