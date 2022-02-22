import requests
import random

def send_otp(mobile,otp):
    apikey = 'B20C32EA27C21065'
    res = ['Hello','Hi','Welcome','otp']
    rand = random.choice(res)
    message = 'Your otp is '+str(otp)+'  will expire in 5 minutes'
    URL  = 'http://sms.itbizcon.com/sms/sendsms.jsp?apikey='+apikey+'&sms=Welcome to DFO Team  '+message+'%20sms&mobiles=+91'+mobile
    x = requests.get(URL)
    print(x.status_code)
    return x.status_code




