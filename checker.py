from selenium import webdriver
from apscheduler.schedulers.blocking import BlockingScheduler
import smtplib, ssl

# site_to_check = 'https://www.fivebelow.com/products/squishmallows-gummy-pal-candy-7oz'
# site_to_check = "https://www.fivebelow.com/products/squishmallows-9in-spring-collection-5"
site_to_check = "https://www.fivebelow.com/"

port = 465  # For SSL
password = "Pineapple12"

sender_email = "squishmallow.notifier@gmail.com"
receiver_email = "colinjmass@gmail.com"
message = f"""\
    Subject: Hi there

    Your item is in stock at {site_to_check}."""

def check_5_below():
    # Create a secure SSL context
    context = ssl.create_default_context()

    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(site_to_check)

    print(driver.title)
    el = driver.find_element_by_tag_name('body')
    str = el.text
    if (str.find("sold out") != -1):
        print("It's still not available my guy")
    else:
        print("Its available")

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login("squishmallow.notifier@gmail.com", password)
            server.sendmail(sender_email, receiver_email, message)

    driver.close()

# check_5_below()
# scheduler = BlockingScheduler()
# scheduler.add_job(check_5_below, 'interval', hours=1)
# scheduler.start()
# check_5_below()
