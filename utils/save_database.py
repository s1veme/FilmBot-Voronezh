import os
import smtplib
import zipfile
import datetime

from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText


EMAIL_USER = os.environ.get('EMAIL_USER')

EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

now = datetime.datetime.now()

date = now.strftime("%d-%m-%Y")


class SendMail():

    def __init__(self, mail, password, date, title_zip='database.zip'):
        self.msg = MIMEMultipart()
        self.mail = mail
        self.password = password

        self.body_part = MIMEText(self.mail, 'plain')

        self.date = date

        self.title_zip = title_zip

    def create_message(self):
        self.msg['Subject'] = self.date
        self.msg['From'] = EMAIL_USER
        self.msg['To'] = EMAIL_USER

        self.msg.attach(self.body_part)

        self._pin_zip()

    def send_message(self):
        smtp_obj = smtplib.SMTP('smtp.mail.ru')

        smtp_obj.ehlo()
        smtp_obj.starttls()
        smtp_obj.ehlo()

        smtp_obj.login(self.mail, self.password)

        smtp_obj.sendmail(self.msg['From'],
                          self.msg['To'], self.msg.as_string())
        smtp_obj.quit()

    def _pin_zip(self):
        with open(f'{self.title_zip}', 'rb') as file:
            self.msg.attach(MIMEApplication(file.read(), Name=self.title_zip))


def create_zip(title_zip='database.zip', title_file='users.db'):
    jungle_zip = zipfile.ZipFile(title_zip, 'w')
    jungle_zip.write(title_file, compress_type=zipfile.ZIP_DEFLATED)
    jungle_zip.close()


def write_log_save_db(date):
    with open('logs/save_db.log', 'a', encoding='utf-8') as file:
        file.write(date)


def main():
    create_zip()

    mail = SendMail(EMAIL_USER, EMAIL_PASSWORD, date)
    mail.create_message()
    mail.send_message()

    write_log_save_db(date)


if __name__ == '__main__':
    main()
