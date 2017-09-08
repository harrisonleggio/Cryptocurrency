import requests
import time
import matplotlib.pyplot as plt
from io import BytesIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64
from datetime import datetime, timedelta

to_address = '9144737958@mms.att.net'
from_address = 'harrisonleggio@my.uri.edu'


def get_prices():
    start = datetime.now() - timedelta(minutes=29)
    end = datetime.now()

    start = start.isoformat()
    end = end.isoformat()

    url = 'https://api.gdax.com/products/ltc-usd/candles?start={}&end={}&granularity=60'.format(start, end)
    print url

    response = requests.get(url)
    data = response.json()
    prices = []
    ticks = range(1, 31)[::-1]

    print ticks

    for i in data:
        prices.append(i[-2])

    print prices
    print len(prices)

    plt.plot(ticks, prices)

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    mail = MIMEMultipart()
    mail['Subject'] = 'LTC Update'
    mail['From'] = from_address
    mail['To'] = to_address
    mail.attach(MIMEText('Max Price: {}\nMin Price: {}'.format(max(prices), min(prices))))

    part = MIMEBase('application', "octet-stream")
    part.set_payload(buf.read())
    encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % 'anything.png')
    mail.attach(part)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.login('harrisonleggio@my.uri.edu', 'k7v912zq6y')
    s.sendmail(from_address, to_address, mail.as_string())
    s.quit()
    print 'Email sent'


if __name__ == '__main__':
    get_prices()