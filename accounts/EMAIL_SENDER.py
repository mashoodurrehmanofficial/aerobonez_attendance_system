
email= "smkbukitmewah2021@gmail.com"
password= "sbmnea4090"
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
  
 
 
def SEND_MESSAGE(recipient,incoming_messgae):
    message = incoming_messgae
    msg = MIMEMultipart()
    msg['From'] = email
    msg['Subject'] = 'Reset link'  
    msg['To'] = recipient
    msg.attach(MIMEText(message))
    try:
        mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(email, password)
        mailServer.sendmail(email, recipient, msg.as_string())
        mailServer.close()
        print ('Email sent!')

    except:
        print ('Something went wrong...')




