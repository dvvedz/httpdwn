from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
import os
import hashlib
import requests
import sys
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def screenshot(subdomain, hashi):
    Path("./screenshots").mkdir(parents=True, exist_ok=True)

    os.environ['WDM_PRINT_FIRST_LINE'] = 'False' # Fungerar ej - Known problem: den printar en tom linje
    os.environ['WDM_LOG_LEVEL'] = '0' # Hide webdriver-manager output

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=OFF")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options, service_log_path=os.devnull)

    driver.set_window_size(1000, 700)
    driver.get(subdomain)
    driver.save_screenshot(f"./screenshots/{hashi}.png")

    driver.close()
    

def download(subdomain):
    try:
        # set random user-agent
        ua = UserAgent()
        headers = {"user-agent": ua.random}
        r = requests.get(subdomain, timeout=10, headers=headers)
        r.encoding = r.apparent_encoding
        combined_str = f"{subdomain} [{r.status_code}]\n\n{r.headers}\n\n{r.text}"

    except ConnectionError:
        return "Connection Error"
    except TimeoutError:
        return "Timeout error 10s"
    except requests.exceptions.ConnectionError:
        return "Connection Error"
    except requests.exceptions.RequestException:
        return "Error"

    return combined_str


def save(subdomain, text):
    # I need the @subdomain to name the file 
    # @text is a string with the request data in it 

    Path("./html/").mkdir(parents=True, exist_ok=True)
    fname_hash = hashlib.md5(subdomain.encode("utf-8")).hexdigest()

    with open(f"./html/{fname_hash}", "w") as f:
        f.write(text)

    return fname_hash


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            for line in f: 
                line = line.rstrip()
                print(f"{save(line, download(line))} {line} ")
    
                save(line, download(line))
                screenshot(line, save(line, download(line)))

    # read from stdin - this part is for paralleization
    else:
        for lin in sys.stdin:
            lin = lin.rstrip()
            print(f"{save(lin, download(lin))} {lin} ")

            save(lin, download(lin))
            screenshot(lin, save(lin, download(lin)))
