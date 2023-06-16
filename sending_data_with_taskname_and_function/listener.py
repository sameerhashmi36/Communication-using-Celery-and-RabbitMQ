#####################################11111111################################

from celery import Celery
import pyotp

# Create a Celery app
app = Celery('listener', broker='amqp://guest:guest@localhost:5672//')

# Configure Redis result backend
app.conf.update(
    result_backend='redis://localhost:6379/0',
)

@app.task
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
    app.worker_main(['worker', '--loglevel=info'])

