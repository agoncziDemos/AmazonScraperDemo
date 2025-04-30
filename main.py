import random
import smtplib
from email.message import EmailMessage

import requests
from bs4 import BeautifulSoup

PRODUCT_URL = "https://www.amazon.com/Quencher-Cupholder-Compatible-Insulated-Stainless/dp/B0DCDQ1RFV/"


def get_random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    ]
    return random.choice(user_agents)


def get_headers():
    return {
        'User-Agent': get_random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }


def get_cookies():
    return {
        'session-id': ''.join(random.choices('0123456789-', k=20)),
        'ubid-main': ''.join(random.choices('0123456789', k=13)),
        'x-main': ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=20))
    }


def get_price():
    session = requests.Session()
    response = session.get(PRODUCT_URL, headers=get_headers(), cookies=get_cookies())
    try:
        soup = BeautifulSoup(response.text, "html.parser")

        # Get product title
        title = soup.find("span", id="productTitle").text.strip()

        # Get price
        price_whole = soup.find("span", class_="a-price-whole").text.split('.')[0]
        price_fraction = soup.find("span", class_="a-price-fraction").text

        # Format price
        price = float(f"{price_whole}.{price_fraction}")

        print(f"Product: {title}")
        print(f"Price: ${price:.2f}")

        with open("docs/price.txt", "w") as f:
            f.write(f"Product: {title}")
            f.write("")
            f.write(f"{title}\nPrice: ${price}")
            print("")
            print("Done creating price file!")

    except AttributeError:
        print("Failed to parse product information.")


def send_alert(email, password, product_name, price):
    msg = EmailMessage()
    msg["Subject"] = f"Price Drop Alert: {product_name}"
    msg["From"] = email
    msg["To"] = email
    msg.set_content(f"{product_name} is now ${price}\n{PRODUCT_URL}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email, password)
            smtp.send_message(msg)
        print("Alert email sent!")
    except Exception as e:
        print(f"Failed to send email: {e}")


if __name__ == "__main__":
    get_price()
