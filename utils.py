import re
from urllib.parse import parse_qs, urlparse


def get_locale_from_url(url: str) -> str:
    return re.search(r'\/([a-z]{2}-[a-z]{2})\/', url).group(1)


def get_skus_from_url(url: str) -> list:
    try:
        parsed_url = urlparse(url)
        fragment = parsed_url.fragment
        skus_param = parse_qs(fragment).get('skus')

        if skus_param:
            skus = skus_param[0].split(',')
            return skus
        else:
            print("No skus parameter found in the URL fragment.")
            return None

    except Exception as e:
        print(f"Error parsing URL: {e}")
        return None
