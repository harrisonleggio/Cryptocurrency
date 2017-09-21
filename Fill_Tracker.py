import hmac, hashlib, time, requests, base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def authenticate():

    api_key = '<api key>'
    secret_key = '<secret key>'
    passphrase = '<passphrase>'
    api_url = 'https://api.gdax.com/fills'

    timestamp = str(time.time())
    request_type = api_url.split('.com/')[1]
    message = '{}GET/{}'.format(timestamp, request_type)
    hmac_key = base64.b64decode(secret_key)
    signature = hmac.new(hmac_key, message, hashlib.sha256)
    signature_b64 = signature.digest().encode('base64').rstrip('\n')

    headers = {
                'CB-ACCESS-SIGN': signature_b64,
                'CB-ACCESS-TIMESTAMP': timestamp,
                'CB-ACCESS-KEY': api_key,
                'CB-ACCESS-PASSPHRASE': passphrase,
                'Content-Type': 'application/json'
                }

    r = requests.get(api_url, headers=headers)
    return r.json()


def write_logfile(fill_count):
    with open('log.txt', 'a') as logfile:
        logfile.write(str(fill_count) + '\n')


def check_fills(data):
    with open('log.txt', 'r') as logfile:
        fills = [x.strip('\n') for x in logfile.readlines()]
    previous_count = fills[-2]
    current_count = fills[-1]

    delta = int(current_count) - int(previous_count)

    if current_count == previous_count:
        return

    print 'Your most recent order has filled'

    new_fills = []
 
    if delta == 1:
        new_fills.append(data[0])
    else:
        for i in range(0, delta):
            new_fills.append(data[i])
   
    text_body = []

    for i in new_fills:
        text_body.append('{}: {} LTC at {}\nTotal:{}'.format(str(i['side']), str(i['size']), str(i['price']), str(float(i['size']) * float(i['price']))))

    to_address = '<sms email address>'
    from_address = 'LTC Update'

    mail = MIMEMultipart()
    mail['Subject'] = 'LTC Update'
    mail['From'] = from_address
    mail['To'] = to_address
    mail.attach(MIMEText('\n'.join(text_body)))

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.login('<sending gmail>', '<sending password>')
    s.sendmail(from_address, to_address, mail.as_string())
    s.quit()

if __name__ == '__main__':
    data = authenticate()
    write_logfile(len(data))
    check_fills(data)
