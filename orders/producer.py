import json 
import pika

# rabbitmq connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat=600, blocked_connection_timeout=300))
channel = connection.channel()

def publish(method, body):

    """
        used to publish request to queue with data
    """  
    
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='orders', body=json.dumps(body), properties=properties)