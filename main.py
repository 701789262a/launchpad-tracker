from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

def main():
    url = 'https://launchpad.binance.com/en/viewall/lpd'
    driver = webdriver.Opera(executable_path=r"operadriver.exe")
    with open("sequence.txt") as f:
        for line in f:
            pass
        last_line = line
    while True:
        driver.get(url)
        WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div/div[3]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div')))
        launchpad_coin=driver.find_element(By.XPATH,'/html/body/div[1]/main/div/div[3]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div').text
        print(launchpad_coin,last_line)
        if launchpad_coin != last_line.strip():
            print("NUOVO LAUNCHPAD")
            with open("sequence.txt", "a") as f:
                f.write(launchpad_coin+'\n')
            with open("sequence.txt") as f:
                for line in f:
                    pass
                last_line = line

if __name__ == "__main__":
    main()