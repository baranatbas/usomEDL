import requests
import os

BASE_URL = "https://www.usom.gov.tr/api/address/index"
PER_PAGE = 5000
TYPES = ["domain", "url", "ip"]

headers = {"User-Agent": "Mozilla/5.0"}

def fetch_type(ioc_type):
    page = 0
    results = []

    while True:
        params = {
            "type": ioc_type,
            "page": page,
            "per-page": PER_PAGE
        }

        r = requests.get(BASE_URL, params=params, headers=headers, timeout=60)
        r.raise_for_status()
        data = r.json()

        models = data.get("models", [])
        if not models:
            break

        for item in models:
            value = item.get("url")
            if value:
                results.append(value.strip())

        page_count = data.get("pageCount", 1)
        page += 1

        if page >= page_count:
            break

    return sorted(set(results))

def main():
    os.makedirs("lists", exist_ok=True)

    domains = fetch_type("domain")
    urls = fetch_type("url")
    ips = fetch_type("ip")

    with open("lists/url-edl.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(domains + urls))

    with open("lists/ip-edl.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(ips))

    print(f"Domain: {len(domains)}")
    print(f"URL: {len(urls)}")
    print(f"IP: {len(ips)}")

if __name__ == "__main__":
    main()
