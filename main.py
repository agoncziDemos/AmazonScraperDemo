import os
import requests
from bs4 import BeautifulSoup
# from dotenv import load_dotenv

# Load email credentials from .env file
# load_dotenv()
# EMAIL = os.getenv("GMAIL_USER")
# PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
EMAIL = ""
PASSWORD = ""

# Configure these before running
PRODUCT_URL = "https://www.amazon.com/Quencher-Cupholder-Compatible-Insulated-Stainless/dp/B0DCDQ1RFV/"


def track_price():
    # Configure headers to mimic a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        response = requests.get(PRODUCT_URL, headers=headers)
        response.raise_for_status()  # Check for HTTP errors

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract price (Amazon's class may change - adjust if needed)
        price_span = soup.find("span", class_="a-offscreen")
        price = float(price_span.text.replace("$", "").replace(",", "")) if price_span else None

        # Extract product title
        title = soup.find("span", id="productTitle").text.strip()

        if price:
            # Print title and price
            print(title)
            print("Price: $" + str(price))

    except Exception as e:
        print(f"Error: {e}")


def send_alert(product_name, price):
    import smtplib
    from email.message import EmailMessage

    msg = EmailMessage()
    msg["Subject"] = f"Price Drop Alert: {product_name}"
    msg["From"] = EMAIL
    msg["To"] = EMAIL
    msg.set_content(f"{product_name} is now ${price}\n{PRODUCT_URL}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL, PASSWORD)
            smtp.send_message(msg)
        print("Alert email sent!")
    except Exception as e:
        print(f"Failed to send email: {e}")


if __name__ == "__main__":
    track_price()
