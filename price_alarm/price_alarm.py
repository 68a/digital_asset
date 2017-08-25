import traceback
import time
import requests
import sys
import datetime
from time import sleep
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import os
import re

from app.utils import *
from price_detect import *

sender_email = ''
sender_email_password = ''
receiver_email = ''

g_cny_rate = 6.65
g_diff_on = 1
g_diff_value = 4.0
g_minus_diff_value = 2.0
g_db_file = './app/data.db'

def read_settings ():
    global g_cny_rate
    global g_diff_on
    global g_diff_value
    global g_minus_diff_value
    
    conn = open_db (g_db_file)
    settings = read_settings_table (conn)
    close_db (conn)
    
    g_cny_rate = float (settings [0] [0]) 
    g_diff_on = settings [0] [1]
    g_diff_value = float (settings [0] [2])
    g_minus_diff_value = - float (settings [0] [3])
    
def get_config():
    global sender_email, sender_email_password, receiver_email

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

def cal(cny_rate, price1, price2):
    price1_cny = price1 * cny_rate
    diff_price = price2 - price1_cny
    diff_price_rate = diff_price / price1_cny
    return diff_price_rate

def check_price (exchanger, pair, cny_rate):
#    time1, btce_price = get_exchanger_price ('btce', pair)
    base_exchanger = 'bitstamp'
#    if pair == 'eth_cny':
#        return base_exchanger, 0, 0, 0
    time1, base_price = get_exchanger_price (base_exchanger, pair)    
    time2, exchanger_price = get_exchanger_price (exchanger, pair)
    diff = cal (cny_rate, base_price, exchanger_price) * 100

    return base_exchanger, diff, exchanger_price, base_price
    
def get_exchanger_diff (exchanger, pair, cny_rate):
    global g_cny_rate
    base_exchanger, diff, exchanger_price, base_price = check_price (exchanger, pair, cny_rate) 
    check_str = '%s %s %.2f %.2f %s: %.2f rate: %.2f' % (exchanger, pair, diff, exchanger_price, base_exchanger, base_price, g_cny_rate)

    return check_str, diff
    

def check_diff_price(cny_rate, min_diff, minus_diff_value):

    base_exchangers_pairs = [ {'name':'bitstamp', 'pairs': ['btc', 'ltc']}]
    target_exchangers =[ {'name': 'yunbi', 'pairs' :[ 'btc', 'ltc', 'eth']},
                          {'name': 'chbtc', 'pairs' : ['btc', 'ltc']} ]
                          
                           
    try:
        diff_list = []

        base = 'bitstamp'

        diff_str, diff = get_exchanger_diff ('yunbi', 'eth_cny', cny_rate)
        diff_list.append ((diff_str, diff) )
        diff_str, diff = get_exchanger_diff ('chbtc', 'btc_cny', cny_rate)
        diff_list.append ((diff_str, diff) )
        diff_str, diff = get_exchanger_diff ('chbtc', 'eth_cny', cny_rate)
        diff_list.append ((diff_str, diff) )
        diff_str, diff = get_exchanger_diff ('chbtc', 'ltc_cny', cny_rate)
        diff_list.append ((diff_str, diff) )


        for d in diff_list:
            print('->', d[1])
            print('min_diff', min_diff, 'minus_diff_value', minus_diff_value)
            if d [1] > min_diff or d [1] < g_minus_diff_value:
                print('>>>', d[0])
                send_email(d[0])                
        
    except:
        type, value, traceback1 = sys.exc_info()
        print (type, value, traceback1)
        traceback.print_exc()

def watch_price ():
    global g_cny_rate, g_diff_value, g_minus_diff_value
    wait_time = 60 * 2
    while True:
        read_settings ()
        if g_diff_on == 1:
            check_diff_price (g_cny_rate, g_diff_value, g_minus_diff_value)
        sleep (wait_time)

if __name__ == '__main__':
    g_db_file = sys.argv[1]
    get_config()
    watch_price ()
