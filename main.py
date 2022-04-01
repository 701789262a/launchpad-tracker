import json
import time
from threading import Thread
from PIL import Image, ImageGrab
import time
import pytesseract
import yaml
from binance import Client
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def main():
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    url = 'https://launchpad.binance.com/en'
    driver = webdriver.Opera(executable_path=r"operadriver.exe")
    with open("sequence.txt") as f:
        for line in f:
            pass
        last_line = line
    with open("key.yaml") as f:
        t = yaml.safe_load(f)
        f.close()
    client = Client(t['bnb_apikey'], t['bnb_secret'])
    while True:
        driver.delete_all_cookies()
        driver.get(url)
        WebDriverWait(driver, 3).until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[1]/main/div/div[1]/div/div[2]/div/div[2]/div[1]')))
        image = screen()
        launchpad_coin = tess(image).strip().replace('\n', '')
        print(launchpad_coin)
        if launchpad_coin != last_line.strip():
            print("NUOVO LAUNCHPAD")
            with open("sequence.txt", "a") as f:
                f.write(launchpad_coin + '\n')
            with open("sequence.txt") as f:
                for line in f:
                    pass
                last_line = line
            if True:
                a = Thread(target=buysellfunc, args=(client, t))
                a.start()
                a.join()


def screen():
    image = ImageGrab.grab(bbox=(865,388,1100,490))
    # image.save(str(int(time.time()))+'.jpg')
    return image


def tess(image):
    text = pytesseract.image_to_string(image)
    return text


def buysellfunc(client, t):
    print("buy")
    reit = 0  # counts reiteration of while cycle
    order = json.loads(client.order_market_buy(
        symbol=t['symbol'],
        quantity=round(float(t['amount']), 5)
    ))
    medium_price = order['price']
    order_sell = json.loads(client.order_limit_sell(
        symbol=t['symbol'],
        quantity=round(float(t['amount']), 5),
        price=medium_price * float(t['required_spread'])
    ))
    while not order_sell['status'] == 'FILLED':
        reit += 1
        order_sell = client.get_order(symbol='BNBUSDT', orderId=order_sell['orderId'])
        time.sleep(0.1)
        if reit > int(t['time_to_liquidate']):
            order_sell = json.loads(client.order_market_sell(
                symbol=t['symbol'],
                quantity=round(float(t['amount']), 5)
            ))
            time.sleep(1)

    print(order['price'], order['origQty'], float(order['price']) * float(order['origQty']), order['status'])
    print(order_sell['price'], order_sell['origQty'], float(order_sell['price']) * float(order_sell['origQty']),
          order_sell['status'])
    print(
        (float(order_sell['price']) * float(order_sell['origQty'])) - (float(order['price']) * float(order['origQty'])))


if __name__ == "__main__":
    main()
