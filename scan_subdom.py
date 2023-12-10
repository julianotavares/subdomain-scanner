import requests
import sys
from concurrent.futures import ThreadPoolExecutor

def find_vhost(url, headers, wordlist):
    try:
        with open(wordlist, 'r') as file:
            for line in file:
                subdomain = line.strip()
                target_url = f"https://{subdomain}.{url}"
                try:
                    response = requests.get(target_url, headers=headers, timeout=5)
                    if response.ok:
                        print(f"[+] {target_url} found with status code {response.status_code}")
                except requests.exceptions.RequestException as e:
                    pass
                except Exception as e:
                    print(e)
                except KeyboardInterrupt:
                    print(f"[!] Error: {str(e)}")
                    sys.exit(1)
    except Exception as e:
        print(e)

if len(sys.argv) < 3:
    print("Usage: python3 subdomain_search.py <domain> <wordlist>")
    sys.exit(1)

domain = sys.argv[1]
wordlist = sys.argv[2]

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Referer': 'https://www.google.com/'
}

with ThreadPoolExecutor(max_workers=10) as executor:
    executor.submit(find_vhost, domain, headers, wordlist)