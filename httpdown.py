from pathlib import Path
import os
import json
import hashlib
import requests
import sys
from fake_useragent import UserAgent


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
    # this part is for paralleization
    else:
        for lin in sys.stdin:
            lin = lin.rstrip()
            print(f"{save(lin, download(lin))} {lin} ")

            save(lin, download(lin))

