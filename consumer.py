import json
import pika
from reportlab.pdfgen.canvas import Canvas
from neurobikes.settings import MEDIA_ROOT


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat=600, blocked_connection_timeout=300))
channel = connection.channel()
channel.queue_declare(queue='orders')


def callback(ch, method, properties, body):

    """
        This function generated a pdf and stores it in media/pdf folder
        Triggered on placing an order
    """

    print(">>> Received order")
    data = json.loads(body)

    if (data):

        username = data.get('user')
        full_name = data.get('full_name')
        bike_model_number = data.get('bike')
        category = data.get('category')
        color = data.get('color')
        amount = data.get('amount')
        payment_type = data.get('payment_type')
        payment_id_number = data.get('payment_id')

        if properties.content_type == 'order_created':

            try:
                canvas = Canvas(MEDIA_ROOT + '/pdf/' + bike_model_number + '_' + username + '.pdf')
                canvas.drawString(10, 700, 'NEUROBIKES SHOP - INVOICE')
                canvas.drawString(10, 600, 'Full Name : ' + full_name)
                canvas.drawString(10, 580, 'Username : ' + username)
                canvas.drawString(10, 560, 'Bike Model Number : ' + bike_model_number)
                canvas.drawString(10, 540, 'Bike Category : ' + category)
                canvas.drawString(10, 520, 'Bike Color : ' + color)
                canvas.drawString(10, 500, 'Amount Paid : ' + str(amount))
                canvas.drawString(10, 480, 'Payment Type : ' + payment_type)
                canvas.drawString(10, 460, 'Payment ID Number : ' + str(payment_id_number))
                canvas.save()
                print(">>> PDF Created")
            except Exception as e:
                print(f">>> {e}")

    else:
        print(">>> Invalid Data Content Received")

channel.basic_consume(queue='orders', on_message_callback=callback, auto_ack=True)
print("Started Consuming...")
channel.start_consuming()