import argparse
import json
from datetime import datetime

import requests

from utils import (get_discounted_games, get_locale_from_url,
                   get_skus_from_url, print_discounted_games)

LOCALE_MAP = {'es-pe': 'es_PE', 'en-us': 'en_US'}


def main(wishlist_url: str, api_endpoint: str, extensions: dict, headers: dict):

    locale_url = get_locale_from_url(wishlist_url)
    locale = LOCALE_MAP.get(locale_url)
    skus = get_skus_from_url(wishlist_url)

    variables = {
        "locale": locale,
        "where": {
            "sku": {
                "in": skus
            }
        }
    }
    variables_str = json.dumps(variables, separators=(',', ':'))

    extensions_str = json.dumps(extensions, separators=(',', ':'))

    params = {
        "operationName": "StoreProducts",
        "variables": variables_str,
        "extensions": extensions_str
    }
    response = requests.request("GET", api_endpoint,
                                params=params,
                                headers=headers)

    if response.status_code == 200:
        games_info = response.json()
        current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")

        with open(f'{current_datetime}-wishlist_games.json', 'w') as file:
            json.dump(games_info, file)

        discounted_games = get_discounted_games(games_info)

        print_discounted_games(discounted_games, locale_url)

    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Nintendo eShop wishlist alert")
    parser.add_argument("--wishlist_url",
                        help="Wishlist URL, shared from https://www.nintendo.com/wish-list/",
                        required=True)
    parser.add_argument("--request_config",
                        help="JSON file with config for games info request",
                        required=True)

    args = parser.parse_args()

    with open(args.request_config, 'r') as file:
        config = json.load(file)

    main(wishlist_url=args.wishlist_url,
         api_endpoint=config['api_endpoint'],
         extensions=config['extensions'],
         headers=config['headers'])
