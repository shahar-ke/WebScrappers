import datetime
import urllib.request
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
    'chamonix':0,
    'argentiere':0,
    'chalet-les-pelerins':0,
    'Chalet Pelerins':0,
    'flaine':0,
    'la-plagne':0,
    'La Plagne':0,
    'les-arcs':0,
    'Les Arcs':0,
    'les-contamines':0,
    'Les Contamines':0,
    'les-deux-alpes':0,
    'Les Deux Alpes':0,
    'serre-chevalier':0,
    'Serre Chevalier':0,
    'Tignes':0,
    "val-d'isere":0,
    "Val d'Isere":0,
    'val-thorens':0,
    "Val Thorens":0,
    'special':0
}


def get_password():
    with open('./password') as password_file:
        password = password_file.read()
    return password.strip()


def send_mail(email_msg):
    target_mail = 'deep_flame@yahoo.com'
    import smtplib
    fromMy = target_mail
    # fun-fact: from is a keyword in python, you can't use it as variable, did anyone check if this code even works?
    to = target_mail
    subj = 'ucpa'
    date = datetime.datetime.now()
    message_text = email_msg

    msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % (fromMy, to, subj, date, message_text)

    username = str(target_mail)
    password = get_password()
    server = smtplib.SMTP("smtp.mail.yahoo.com", 587)
    server.starttls()
    server.login(username, password)
    server.sendmail(fromMy, to, msg)
    server.quit()


def main():
    try:
        url = "https://www.action-outdoors.co.uk/winter/deals/special-offers"
        page = download(url)
        page = page.decode("utf-8")
        assert isinstance(page, str)
        found = dict()
        for key in EXPECTED:
            found[key] = 0
        for line in page.splitlines():
            line = line.strip()
            if not line:
                continue
            for key in sorted(EXPECTED.keys()):
                if key.lower() in line:
                    found[key] += 1
        email_msg = list()
        for key in sorted(EXPECTED.keys()):
            if found[key] != EXPECTED[key]:
                email_msg.append("%s, expected:%d, found:%d" % (key, EXPECTED[key], found[key]))
    except Exception as e:
        email_msg.clear()
        email_msg.append('exception was thrown')
        email_msg.append(str(e))
    if email_msg:
        email_msg.insert(0, 'pay attention !')
        send_mail('\n'.join(email_msg))
        print('email sent')


if __name__ == "__main__":
    main()