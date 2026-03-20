# utils/email_sender.py
import smtplib
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from constants import EMAIL_CONFIG

def send_email_async(recipient, subject, body):
    def task():
        try:
            server = smtplib.SMTP(EMAIL_CONFIG["smtp_server"], EMAIL_CONFIG["smtp_port"])
            if EMAIL_CONFIG.get("use_tls", True):
                server.starttls()
            server.login(EMAIL_CONFIG["sender_email"], EMAIL_CONFIG["sender_password"])
            msg = MIMEMultipart()
            msg["From"] = EMAIL_CONFIG["sender_email"]
            msg["To"] = recipient
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))
            server.send_message(msg)
            server.quit()
            print(f"Correo enviado a {recipient}")
        except Exception as e:
            print(f"Error enviando correo: {e}")

    thread = threading.Thread(target=task)
    thread.daemon = True  # se cierra cuando la app principal termina
    thread.start()

def send_verification_email(recipient, code):
    subject = "Verificación de registro - Biblioteca Digital"
    body = f"Hola,\n\nPara completar tu registro, ingresa el siguiente código de verificación:\n\n{code}\n\nEste código expira en 10 minutos.\n\nSaludos."
    send_email_async(recipient, subject, body)

def send_welcome_email(user_email, user_name):
    subject = "Bienvenido a Biblioteca Digital"
    body = f"Hola {user_name},\n\nGracias por registrarte en nuestra biblioteca digital. ¡Disfruta de nuestros servicios!\n\nSaludos."
    send_email_async(user_email, subject, body)