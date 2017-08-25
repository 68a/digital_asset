import time
#import pytz
import requests
import sys
import datetime
from time import sleep
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import os
import re
import hmac
import hashlib

bitstamp_key = ''
bitstamp_secret = ''
sender_email = ''
sender_email_password = ''
receiver_email = ''
bitstamp_customer_id = ''

def get_config():
    global bitstamp_key, bitstamp_secret, bitstamp_customer_id, sender_email, sender_email_password, receiver_email

    bitstamp_key = os.environ['BITSTAMP_KEY']
    bitstamp_secret = os.environ['BITSTAMP_SECRET']
    bitstamp_customer_id = os.environ['BITSTAMP_CUSTOMER_ID']
    sender_email = os.environ['SENDER_EMAIL']
    sender_email_password = os.environ['SENDER_EMAIL_PASSWORD']
    receiver_email = os.environ['RECEIVER_EMAIL']

def send_email(subject_str):
    global receiver_email, sender_email, sender_email_password
    receivers = re.split(r'[, ]*', receiver_email)
    receivers = list(filter(None, receivers))
    print(receivers)

    message = MIMEText(subject_str, 'plain', 'utf-8')
    message['From'] = Header("Bot", 'utf-8')
    message['To'] =  Header('You', 'utf-8')
    subject = subject_str
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL('smtp.qq.com')

        smtpObj.login(sender_email, sender_email_password)
        smtpObj.sendmail(sender_email, receivers, message.as_string())
    except smtplib.SMTPException as e:
        print(e)

def get_bitstamp(balance_types):
    global bitstamp_key, bitstamp_secret, bitstamp_customer_id
    nonce = str(int(time.time()))
    
    message = nonce + bitstamp_customer_id + bitstamp_key

    secret_bytes = bytes (bitstamp_secret, 'latin-1')
    signature = hmac.new(
        bitstamp_secret.encode ('utf-8'),
        msg=message.encode ('utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest().upper()
    
    balance_result = []
    url = 'https://www.bitstamp.net/api/v2/balance/'
    try:
        r = requests.post(url, data = {
            'key': bitstamp_key,
            'signature':signature,
            'nonce': nonce
        }
                         )

        bitstamp_json = r.json()

        for x in balance_types:
            balance_result.append(float(bitstamp_json[x]))

    except:
        print('Failed to get bitstamp!')

    return balance_result

def check_balance(old_balance):
    balance_types = ['usd_balance', 'btc_balance']
    balance_ret = get_bitstamp(balance_types)
    
    if old_balance != balance_ret:
        message = 'BITSTAMP usd:{:,.2f} btc:{:.4f}'.format(balance_ret [0], balance_ret [1])
        print (message)
        send_email(message)
    return balance_ret
          
def watch_balance():
    wait_time = 60 * 1
    old_balance = [0.0, 0.0]

    while True:
        old_balance = check_balance(old_balance)
        sleep(wait_time)


if __name__ == '__main__':
    get_config()
    watch_balance()


