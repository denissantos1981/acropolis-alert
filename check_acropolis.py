import os
import time
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

URL = "https://hhticket.gr/tap_b2c_new/english/tap.exe?PM=P1P&place=000000002"

TARGET_DATE = "24/06"
TARGET_HOURS = ["08", "09", "10", "11"]

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")


def create_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)


def send_email():
    subject = "🚨 Acropolis Ticket Alert"
    body = f"Ingressos disponíveis para {TARGET_DATE} pela manhã!\n{URL}"

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())


def check():
    driver = create_driver()
    driver.get(URL)

    time.sleep(8)

    page = driver.page_source
    driver.quit()

    if TARGET_DATE in page:
        for h in TARGET_HOURS:
            if h in page:
                send_email()
                return


if __name__ == "__main__":
    check()
