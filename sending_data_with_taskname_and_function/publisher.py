from celery import Celery
from kombu import Connection, Exchange, Queue

# Create a Celery app
app = Celery('publisher', broker='amqp://guest:guest@localhost:5672//')

# Configure Redis result backend
app.conf.update(
    result_backend='redis://localhost:6379/0',
)

# Create a custom exchange and queue for phone numbers
phone_exchange = Exchange('phone_exchange', type='direct')
phone_queue = Queue('phone_queue', exchange=phone_exchange, routing_key='phone')

# Configure the app to use the custom exchange and queue
app.conf.task_queues = [phone_queue]


@app.task
def send_phone_number(phone_number):
    # Publish the phone number to the phone_queue
    result = app.send_task('listener.generate_otp', args=[phone_number])
    return result.get()


if __name__ == '__main__':
    # Example usage: python publisher.py +123456789
    import sys

    phone_number = sys.argv[1]
    # result = send_phone_number.delay(phone_number)
    result = app.send_task('listener.generate_otp', args=[phone_number])
    print(result.get())
    if result.successful():
        otp_value = result.result
        print("OTP:", otp_value)
    else:
        print("Error occurred while generating OTP:", result.result)
