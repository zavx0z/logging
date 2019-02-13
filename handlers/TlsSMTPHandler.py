import logging.handlers
from email.header import Header
from email.mime.text import MIMEText


class TlsSMTPHandler(logging.handlers.SMTPHandler):
    def emit(self, record):
        """
        Emit a record.

        Format the record and send it to the specified addressees.
        """
        try:
            import smtplib
            try:
                from email.utils import formatdate
            except ImportError:
                formatdate = self.date_time
            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT
            message = self.format(record)

            msg = MIMEText(message, 'plain', 'utf-8')
            msg['Subject'] = Header(self.getSubject(record), 'utf-8')
            msg['From'] = self.fromaddr
            msg['To'] = ' ,'.join(self.toaddrs)
            msg['Date'] = formatdate()

            smtp = smtplib.SMTP(self.mailhost, port)
            if self.username:
                smtp.ehlo()  # for tls add this line111
                smtp.starttls()  # for tls add this line
                smtp.ehlo()  # for tls add this line
                smtp.login(self.username, self.password)
            smtp.sendmail(self.fromaddr, self.toaddrs, msg.as_string())
            smtp.quit()
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)


if __name__ == '__main__':
    from logging import config

    MAIL_HOST = ("smtp.mail.ru", 587)
    FROM_ADDR = 'zavx0z@inbox.ru'
    TO_ADDR = [
        'zavx0z@ya.ru',
    ]
    SUBJECT = 'Произошла ошибка!'
    EMAIL_LOGIN = 'zavx0z@inbox.ru'
    EMAIL_PASSWORD = 'pass'

    LOG_SETTINGS = {
        'version': 1,
        'handlers': {
            'email': {
                'class': 'loggingSMTP.TlsSMTPHandler',
                'mailhost': MAIL_HOST,
                'fromaddr': FROM_ADDR,
                'toaddrs': TO_ADDR,
                'subject': SUBJECT,
                'credentials': (
                    EMAIL_LOGIN,
                    EMAIL_PASSWORD
                ),
            }
        },
        'loggers': {
            'email': {
                'level': 'ERROR',
                'handlers': ['email']
            }
        }
    }

    logging.config.dictConfig(LOG_SETTINGS)

    email_logger = logging.getLogger('email')

    try:
        1 / 0
    except Exception as ex:
        email_logger.error('любое сообщение об ошибке')
        email_logger.exception('сообщение с трейсом')
