from credentials import sendgrid_creds
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content


class EmailAlerts:
    """
    Class to interact with Twilio's SendGrid API
    """
    def __init__(self):
        self.SENDGRID_API_KEY = sendgrid_creds['SENDGRID_API_KEY']

    def send_email(self, subject, body, sender='raymondt013@gmail.com', recipient='realcoinboys@gmail.com'):
        """
        Method to send email
        :param subject: the email subject line
        :param body: the body of the email
        :param sender: the email address of the sender
        :param recipient: the intended email recipient
        :return:
        """
        try:
            sg = SendGridAPIClient(api_key=self.SENDGRID_API_KEY)
            from_email = Email(sender)
            to_email = To(recipient)
            content = Content("text/plain", body)
            mail = Mail(from_email, to_email, subject, content)

            # Get a JSON-ready representation of the Mail object
            mail_json = mail.get()

            # Send an HTTP POST request to /mail/send
            response = sg.client.mail.send.post(request_body=mail_json)
            print(response.status_code, 'New coin listing email alert sent')
        except Exception as e:
            print(e)
            pass