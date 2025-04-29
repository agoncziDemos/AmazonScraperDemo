from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

PRODUCT_URL = "https://www.amazon.com/Quencher-Cupholder-Compatible-Insulated-Stainless/dp/B0DCDQ1RFV/"


def get_price():
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(PRODUCT_URL)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Get product title
        title = soup.find("span", id="productTitle").text.strip()

        # Get price
        price_whole = soup.find("span", class_="a-price-whole").text.split('.')[0]
        price_fraction = soup.find("span", class_="a-price-fraction").text

        # Format price
        price = float(f"{price_whole}.{price_fraction}")

        print(f"Product: {title}")
        print(f"Price: ${price:.2f}")
    finally:
        driver.quit()


def send_alert(email, password, product_name, price):
    import smtplib
    from email.message import EmailMessage

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
