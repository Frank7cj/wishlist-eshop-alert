import argparse
import json
from datetime import datetime

import requests

from sqlite_connection import SQLiteConnection
from utils import (get_all_time_discounted_games, get_discounted_games,
                   get_locale_from_url, get_skus_from_url, insert_info_games,
                   print_discounted_games)

LOCALE_MAP = {'es-pe': 'es_PE', 'en-us': 'en_US'}

NINTENDO_GAME_COLUMNS = {
    'sku': 'VARCHAR(255)',
    'name': 'VARCHAR(255)',
    'url_key': 'VARCHAR(255)',
    'price': 'DECIMAL(10, 2)',
    'original_price': 'DECIMAL(10, 2)',
    'discount_percentage': 'DECIMAL(5, 2)',
    'discounted': 'BOOLEAN',
    'timestamp_value': 'TIMESTAMP'
}


def main(wishlist_url: str, api_endpoint: str, extensions: dict,
         headers: dict, sqlite_path: str = None, json_export: bool = False):

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
        games_list = games_info['data']['products']
        current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")

        if json_export:
            with open(f'{current_datetime}-wishlist_games.json', 'w') as file:
                json.dump(games_info, file)

        discounted_games = get_discounted_games(games_list)

        all_time_discounted_games = []
        if sqlite_path is not None:
            sqlite_connection = SQLiteConnection(sqlite_path)
            sqlite_connection.connect()

            # Create nintendo_game table if not exists
            sqlite_connection.create_table(
                'wishlist_games', NINTENDO_GAME_COLUMNS)

            insert_info_games(sqlite_connection, games_list)
            all_time_discounted_games = get_all_time_discounted_games(
                sqlite_connection, discounted_games)

            sqlite_connection.close()

        print_discounted_games(
            discounted_games, locale_url, all_time_discounted_games)

    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Nintendo eShop wishlist alert")
    parser.add_argument("--wishlist_url",
                        help="Wishlist URL, shared from https://www.nintendo.com/wish-list/",
                        type=str,
                        required=True)
    parser.add_argument("--request_config",
                        help="JSON file with config for games info request",
                        type=str,
                        required=True)
    parser.add_argument('--sqlite_path',
                        help='Path to .sqlite database file',
                        type=str,
                        required=False)
    parser.add_argument('--json_export',
                        help='Path to export .json file with games info. 1=Yes, 0=No',
                        type=int,
                        required=False)

    args = parser.parse_args()

    with open(args.request_config, 'r') as file:
        config = json.load(file)

    main(wishlist_url=args.wishlist_url,
         api_endpoint=config['api_endpoint'],
         extensions=config['extensions'],
         headers=config['headers'],
         sqlite_path=args.sqlite_path,
         json_export=args.json_export)
