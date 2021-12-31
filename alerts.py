from credentials import sendgrid_creds
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content


class EmailAlerts:
    """
    Class to interact with Twilio's SendGrid API
    """
    def __init__(self):
        self.SENDGRID_API_KEY = sendgrid_creds['SENDGRID_API_KEY']
        self.SENDER = sendgrid_creds['FROM_EMAIL']
        self.RECIPIENT = sendgrid_creds['TO_EMAIL']

    def send_email(self, subject, body):
        """
        Method to send email
        :param subject: the email subject line
        :param body: the body of the email
        :return:
        """
        try:
            sg = SendGridAPIClient(api_key=self.SENDGRID_API_KEY)
            from_email = Email(self.SENDER)
            to_email = To(self.RECIPIENT)
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
