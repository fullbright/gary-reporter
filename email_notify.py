#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python 3 and compatibility with Python 2
from __future__ import unicode_literals, print_function

import os
import sys
import re
import logging
#import smtplib
import requests
import json

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from jinja2 import Environment, FileSystemLoader



class EmailNotification(object):

    EMAIL_REGEX = re.compile('([\w\-\.\']+@(\w[\w\-]+\.)+[\w\-]+)')
    HTML_REGEX = re.compile('(^<!DOCTYPE html.*?>)')

    def __init__(self, smtp, fromuser, fromemail, login=None,
                 password=None, templatedir='templates', logger=None):
        self.logger = logger
        if not logger:
            logging.basicConfig()
            self.logger = logging.getLogger(__name__)
        self.smtp = smtp
        self.fromuser = fromuser
        self.fromemail = fromemail
        self.mfrom = "%s <%s>" % (fromuser, fromemail)
        self.reply = fromemail
        self.smtplogin = login
        self.smtppass = password
        if os.path.isdir(templatedir):
            self.templatedir = templatedir
        else:
            self.templatedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), templatedir)
        self.env = Environment(loader=FileSystemLoader(self.templatedir))


    def _mailrender(self, data, template):
        template = template + ".tmpl"
        self.logger.debug("Rendering template '%s'" % (template))
        text = self.env.get_template(template)
        msg = text.render(data)
        return msg

    def mailgun_emailer(self, data, template):

        self.logger.debug("Loading the information from the config file")
        j = json.loads(open("config.json").read())

        key = j['mailgun_api_key'] #'YOUR API KEY HERE'
        sandbox = j['mailgun_url'] #'YOUR SANDBOX URL HERE'
        self.logger.debug("Mailgin key %s and url %s" % (key, sandbox))

        request_url = 'https://api.mailgun.net/v2/{0}/messages'.format(sandbox)
        self.logger.debug("Request url: %s"  % (request_url))

        recipient = data[0]['email']
        subject = data[0]['subject']
        email_body = self._mailrender(data[0]['data'], template)

        self.logger.debug("Sending email from %s to : %s" % (self.fromemail, recipient))

        request = requests.post(request_url, auth=('api', key), data={
            'from': self.mfrom,
            'to': recipient,
            'subject': subject,
            'html': email_body
        })

        self.logger.debug("Status: %s" % (request.status_code))
        self.logger.debug("Body:   %s" % (request.text))

        return request.text


    def _smtpconnect(self):
        try:
            smtp = smtplib.SMTP(self.smtp)
        except Exception as e:
            self.logger.error("Cannot connect with '%s': %s" % (self.smtp, e))
            raise
        if self.smtplogin:
            try:
                smtp.login(self.smtplogin, self.smtppass)
            except smtplib.SMTPException as e:
                self.logger.error("Cannot auth with '%s' on %s: %s" % (self.smtplogin, self.smtp, e))
                raise
            finally:
                smtp.quit()
        return smtp

    def _smtpsend(self, smtp, recipient, subject, content):
        if self.HTML_REGEX.match(content) is None:
            self.logger.debug("Sending text mail to '%s'" % (recipient))
            msg = MIMEText(content)
        else:
            self.logger.debug("Sending html mail to '%s'" % (recipient))
            msg = MIMEMultipart('alternative')
            msg.attach(MIMEText(content, 'html', 'utf-8'))
        msg['From'] = self.mfrom
        msg['To'] = recipient
        msg['Reply-to'] = self.reply
        msg['Subject'] = subject
        smtp.sendmail(self.mfrom, [recipient], msg.as_string())


    def send_email(self, recipient, subject, msg):
        smtp = self._smtpconnect()
        try:
            self._smtpsend(smtp, recipient, subject, msg)
        except smtplib.SMTPException as e:
            self.logger.error("Cannot send mail to '%s': %s" % (recipient, e))
            raise
        finally:
            smtp.quit()


    def send_bulk(self, msgs):
        smtp = self._smtpconnect()
        processed = 0
        for (recipient, subject, msg) in msgs:
            try:
                self._smtpsend(smtp, recipient, subject, msg)
            except smtplib.SMTPException as e:
                self.logger.error("Cannot send mail to '%s': %s" % (recipient, e))
            else:
                processed += 1
        smtp.quit()
        return processed


    def mailout(self, email, name, subject, data, template):
        if email is None:
            error = "Email is empty!"
            self.logger.error(error)
            raise ValueError(error)
        elif self.EMAIL_REGEX.match(email) is None:
            error = "Invalid email address!"
            self.logger.error(error)
            raise ValueError(error)
        msg = self._mailrender(data, template)
        self.send_email(email, subject, msg)


    def mailbulk(self, email_data, template):
        elist = []
        for edata in email_data:
            try:
                email = edata["email"]
                name = edata["name"]
                subject = edata["subject"]
                data = edata["data"]
            except Exception as e:
                continue
            if email is None:
                error = "Email is empty!"
                self.logger.error(error)
                continue
            elif self.EMAIL_REGEX.match(email) is None:
                error = "Invalid email address!"
                self.logger.error(error)
                continue
            msg = self._mailrender(data, template)
            elist.append((email, subject, msg))
        return self.send_bulk(elist)



def main(argv):
    e = EmailNotification("smtp.example.com", "Jose Riguera", "jriguera@gmail.com")
    elist = [{
    	"email": "jriguera@gmail.com",
    	"name": "Simon",
    	"subject": "Hi",
    	"data" : {
            "dear": "Simon",
            "msg": "Hola mundo"
        }
    }]
    e.mailbulk(elist, "email-html_notify")


if __name__ == "__main__":
    main(sys.argv)
