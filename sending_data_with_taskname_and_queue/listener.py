#####################################11111111################################

from celery import Celery
from kombu import Connection, Exchange, Queue
import pyotp

# Create a Celery app
app = Celery('listener', broker='amqp://guest:guest@localhost:5672//')

# Configure Redis result backend
app.conf.update(
    result_backend='redis://localhost:6379/0',
)

# Create a custom exchange and queue for phone numbers
phone_exchange = Exchange('phone_exchange', type='direct')
phone_queue = Queue('phone_queue', exchange=phone_exchange, routing_key='phone')

# Configure the app to use the custom exchange and queue
app.conf.task_queues = [phone_queue]


@app.task(name='listener', queue=phone_queue)
def generate_otp(phone_number):
    # Replace this with your OTP generation logic
    otp_secret = pyotp.random_base32()
    otp = pyotp.TOTP(otp_secret)
    otp_value = otp.now()
    print(otp_value)
    print("1111111111111111",phone_number)
    return otp_value


if __name__ == '__main__':
    # Start the Celery worker to listen for tasks
    app.worker_main(['worker', '--loglevel=info', '-Q', 'phone_queue'])

