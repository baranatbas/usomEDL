import requests
import xml.etree.ElementTree as ET
import os

XML_URL = "https://www.usom.gov.tr/url-list.xml"

response = requests.get(XML_URL, timeout=60)
response.raise_for_status()

root = ET.fromstring(response.content)

entries = []

for item in root.iter("url-info"):
    url_tag = item.find("url")

    if url_tag is not None and url_tag.text:
        entries.append(url_tag.text.strip())

os.makedirs("lists", exist_ok=True)

with open("lists/url-edl.txt", "w") as f:
    f.write("\n".join(entries))
