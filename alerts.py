from twilio.rest import Client
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



class Twilio:

    def __init__(self, website, error = ''):
        self.website = website
        self.error = error

    def send_alert(self):
        account_sid = 'ACd654cc97633bc7ffe43212e705370d84'
        auth_token = '410753a8ec99c382fb743342c05bcd1e'
        client = Client(account_sid, auth_token)
        numbers_to_message = ['+14052070115']
        for number in numbers_to_message:
                message = client.messages \
                        .create(
                                body= """Warning: %s is down.

                                Error: %s """ % (self.website, self.error),
                                from_='+14056228386',
                                to=number
                            )
        print(message.sid)

    def send_email(self):
        sender_email = "cbh4ou@gmail.com"
        receiver_email = ["connor@jkwenterprises.com", "zach@jkwenterprises.com", "logan@jkwenterprises.com"]
        password = "doabynovtpdoudwz"
        message = MIMEMultipart("alternative")
        message["Subject"] = "Funnel Monitor Report"
        message["From"] = sender_email
        message["To"] = ", ".join(receiver_email)
    # Create the plain-text and HTML version of your message
        text = """\
        Hi,
        How are you?
        Real Python has many great tutorials:
        www.realpython.com"""
        final_string = ''
        final_string += """\

            <p> ***<a href=%s>%s</a>*** : is currently down.
            Error: %s</p>
        """ % (self.website, self.message)

        html = """\
        <html>
                <body>
            <h4>Funnels Down<h4/>
            %s

                </body>
        </html>
        """ % final_string

                # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)
        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )