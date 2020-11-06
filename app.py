from flask import Flask, request
from twilio.rest import Client
from marketstack import get_stock_price
from os import environ

app = Flask(__name__)


ACCOUNT_ID = environ.get('TWILIO_ACCOUNT')
TWILIO_TOKEN = environ.get('TWILIO_TOKEN')
client = Client(ACCOUNT_ID, TWILIO_TOKEN)
TWILIO_NUMBER = 'whatsapp:+14155238886'


def send_msg(msg, recipient):
    client.messages.create(
        from_=TWILIO_NUMBER,
        body=msg,
        to=recipient
    )


def process_msg(msg):
    response = ""
    msg = msg.lower()
    if msg == 'hi':
        response = "Hello, welcome to the stock chatbot! "
        response += "Type quote:<stock_symbol> to get the latest stock price."
    elif "quote:" in msg:
        data = msg.split(":")
        stock_symbol = data[1]
        stock_price = get_stock_price(stock_symbol)
        last_price = stock_price['last_price']
        last_price_str = str(last_price)
        response = "The latest price of " + stock_symbol.upper() + " is $" + \
            last_price_str
    else:
        response = "Please type hi to get started."
    return response


@app.route('/webhook', methods=["POST"])
def webhook():
    f = request.form
    msg = f['Body']
    sender = f['From']
    response = process_msg(msg)
    send_msg(response, sender)
    return "OK", 200
