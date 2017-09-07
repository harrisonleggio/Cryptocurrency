import requests
import time
import matplotlib.pyplot as plt
from io import BytesIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64

to_address = ''
from_address = ''


def get_prices():
    url = 'https://api.gdax.com/products/ltc-usd/ticker'
    counter = 0
    prices = []
    ticks = []

    while counter < 30:
        response = requests.get(url)
        data = response.json()
        prices.append(float(data['price']))
        ticks.append(counter)
        counter += 1
        time.sleep(60)

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
    s.login('', '')
    s.sendmail(from_address, to_address, mail.as_string())
    s.quit()
    print 'Email sent'


if __name__ == '__main__':
    get_prices()
