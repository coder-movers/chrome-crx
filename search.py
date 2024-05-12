import requests
import re

from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}


def search_list(name):
    url = f'https://chromewebstore.google.com/search/{name}?utm_source=ext_app_menu'

    response = requests.get(url=url, headers=headers)
    response.raise_for_status()
    page = response.text
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme
    domain = parsed_url.netloc

    # with open(f"{name}.html", 'r', encoding='utf-8') as f:
    #     page = f.read()

    soup = BeautifulSoup(page, "html.parser")

    tags = soup.find_all(class_="q6LNgd")
    details = {}
    for tag in tags:
        # print(tag)
        href = tag.get('href')

        # TODO：不确定metadata是否需要，先注释
        # jslog = tag.get('jslog')
        # if jslog:
        #     metadata_match = re.search(r'metadata:([^;]+)', jslog)
        #     if metadata_match:
        #         metadata_encoded = metadata_match.group(1)
        #         metadata_decoded = base64.b64decode(metadata_encoded).decode()
        #         print("Metadata:", metadata_decoded)
        #     else:
        #         print("Metadata: No metadata found")
        match = re.search(r'/detail/([^/]+)/([^/]+)$', href)
        if match:
            extension_name = match.group(1)
            detail_url = urljoin(f"{scheme}://{domain}", href)
            details[extension_name] = detail_url

    return details


print(search_list("trans"))
