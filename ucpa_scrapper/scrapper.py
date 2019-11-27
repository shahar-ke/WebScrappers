import argparse
import datetime
import logging
import smtplib
import urllib.request
from logging.handlers import RotatingFileHandler
from urllib.error import URLError, HTTPError, ContentTooShortError


def download(url):
    print('Downloading:', url)
    try:
        html = urllib.request.urlopen(url).read()
    except (URLError, HTTPError, ContentTooShortError) as e:
        print('Download error:', e.reason)
        html = None
    return html


EXPECTED = {
    'chamonix': 3,
    'argentiere': 3,
    'chalet-les-pelerins': 3,
    'Chalet Pelerins': 0,
    'flaine': 4,
    'la-plagne': 4,
    'La Plagne': 0,
    'les-arcs': 4,
    'Les Arcs': 0,
    'les-contamines': 4,
    'Les Contamines': 0,
    'les-deux-alpes': 4,
    'Les Deux Alpes': 0,
    'serre-chevalier': 3,
    'Serre Chevalier': 0,
    'Tignes': 3,
    "val-d'isere": 1,
    "Val d'Isere": 0,
    'val-thorens': 4,
    "Val Thorens": 0,
    'special': 11,
    'lines': 3017
}


def send_mail(email_msg='', email_password=''):
    target_mail = 'deep_flame@yahoo.com'
    from_mail = target_mail
    # fun-fact: from is a keyword in python, you can't use it as variable, did anyone check if this code even works?
    to = target_mail
    subj = 'ucpa'
    date = datetime.datetime.now()
    message_text = email_msg
    msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % (from_mail, to, subj, date, message_text)
    username = str(target_mail)
    password = email_password
    server = smtplib.SMTP("smtp.mail.yahoo.com", 587)
    server.starttls()
    server.login(username, password)
    server.sendmail(from_mail, to, msg)
    server.quit()


def main():
    logger = logging.getLogger(__name__)
    # Create handlers
    s_handler = logging.StreamHandler()
    f_handler = RotatingFileHandler('ucpa_scrapper.log', maxBytes=100000, backupCount=10)
    formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    s_handler.setFormatter(formatter)
    f_handler.setFormatter(formatter)
    logger.addHandler(s_handler)
    logger.addHandler(f_handler)
    logger.setLevel(logging.DEBUG)
    logger.info('program start')
    e = ''
    parser = argparse.ArgumentParser(description='parse ucpa special deals')
    parser.add_argument('--e_pass', dest='e_password', required=True, help='email password', type=str)
    args = parser.parse_args()
    email_msg = list()
    try:
        url = "https://www.action-outdoors.co.uk/winter/deals/special-offers"
        logger.info('fetching info from %s' % (url,))
        page = download(url)
        page = page.decode("utf-8")
        assert isinstance(page, str)
        found = dict()
        for key in EXPECTED:
            found[key] = 0
        lines = 0
        for line in page.splitlines():
            lines += 1
            line = line.strip()
            if not line:
                continue
            for key in sorted(EXPECTED.keys()):
                if key.lower() in line:
                    found[key] += 1
        logger.info('parsed %d lines' % (lines,))
        found['lines'] = lines
        for key in sorted(EXPECTED.keys()):
            if found[key] != EXPECTED[key]:
                msg = "%s, expected:%d, found:%d" % (key, EXPECTED[key], found[key])
                email_msg.append(msg)
                logger.info(msg)
    except Exception as e:
        email_msg.clear()
        err_msg = 'exception was thrown'
        email_msg.append(err_msg)
        logger.error(err_msg)
        exep_msg = str(e)
        email_msg.append(exep_msg)
        logger.error(exep_msg)
    if email_msg:
        email_msg.insert(0, 'pay attention !')
        msg = '\n'.join(email_msg)
        send_mail(email_msg=msg, email_password=args.e_password)
        print(msg)
        print('email sent')
    if e:
        logger.error('raising exception')
        raise e
    logger.info('gracefully done :)')


if __name__ == "__main__":
    main()


