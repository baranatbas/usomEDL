import requests
import os

BASE_URL = "https://siberguvenlik.gov.tr/api/address/index"
PER_PAGE = 5000
TYPES = ["domain", "url", "ip"]

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
}

def fetch_type(ioc_type):
    page = 0
    results = []

    while True:
        params = {
            "type": ioc_type,
            "page": page,
            "per-page": PER_PAGE
        }

        r = requests.get(
            BASE_URL,
            params=params,
            headers=headers,
            timeout=60,
            allow_redirects=True
        )

        r.raise_for_status()

        print("Status:", r.status_code)
        print("URL:", r.url)
        print("Response preview:", r.text[:200])

        data = r.json()

        models = data.get("models", [])

        if not models:
            break

        for item in models:
            value = item.get("url") or item.get("address") or item.get("value")

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

    print("Domain count:", len(domains))
    print("URL count:", len(urls))
    print("IP count:", len(ips))


if __name__ == "__main__":
    main()
