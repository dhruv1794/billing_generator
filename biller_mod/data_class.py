import csv
import datetime
from email.mime.multipart import MIMIMultipart
from email.mime.text import MIMEText
import smtplib
import shutil
import os
from tempfile import NamedTemporaryFile
from utils.templates import get_template, render_context

file_item_path= os.path.join(os.path.dirname(_file_), "data.csv")


host = "smtp.gmail.com"
port =587
username = "pyhtonlearning1994@gmail.com"
password = "Dhruv1794@"
from_email = username
to_list = []
class UserManager():
    def render_message(self, user_data):
        file_ = 'templates/email_message.txt'
        file_html = 'templates/email_message.html'
        if isinstance(user_data, dict):
            context = user_data
            plain_ = render_context(template context)
            html_ = render_context(template_html, context)
            return (plain_, html_)
        return (None,None)

    def message_user(self, user_id=None, email=None, subject='billing update!'):
        user = self.get_user_data(user_id=user_id, email=email)
        if user:
            plain_,html_ = self.render_message(user)
            print(plain_, html_)
            user_email = user.get("email", "pyhtonlearning1994@gmail.com")
            to_list.append(user_email)
            try:
                email_conn = smtplib.SMTP(host, port)
                email_conn.ehlo()
                email_conn.starttls()
                email_conn.login(username, password)
                the_msg = MIMEMultipart("alternative")
                the_msg['subject'] = subject
                the_msg['from'] = username
                the_msg['to'] = user_email
                part_1 = MIMEText(plain_, 'plain')
                part_2 = MIMEText(html_, "html")
                the_msg.attach(part_1)
                the_msg.attach(part_2)
                email_conn.sendmail(from_mail, to_list, the_msg.as_string())
                email_conn.quit()
            except smtplib.SMTPException:
                print("error sending message")
        return None

    def get_user_data(self, user_id=None, email=None):
        filename = file_item_path
        with open(filename, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            items = []
            unknown_user_id = None
            unknown_email = None
            for row in reader:
                if user_id is not None:
                    if int(user_id) == int(row.get('id')):
                        return row 
                    else:
                        unknown_user_id = user_id
                if email is not None:
                    if email == row["email"]:
                        return row 
                    else:
                        unknown_email = email
                if unknown_user_id is not None:
                    print("user id {user_id} not found".format(user_id=user_id))
                if unknown_email is not None:
                    print("email {email} not fount".format(email=email))
            return None
        
