from datetime import datetime
import re
from urllib.parse import parse_qs, urlparse

from sqlite_connection import SQLiteConnection


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


def get_discounted_games(games_list: dict) -> list:
    discounted_games = []

    for game in games_list:
        price = game['prices']['minimum']
        if price['discounted']:
            discounted_games.append(game)

    return discounted_games


def print_discounted_games(discounted_games: list, locale_url: str,
                           all_time_discounted_games: list = []):
    print('-'*100)
    print("! Alert Nintendo eShop game(s) in discount\n")
    for game in discounted_games:
        print(
            f"{game['name']} | https://www.nintendo.com/{locale_url}/store/products/{game['urlKey']}")
        price = game['prices']['minimum']
        all_time_discounted_flag = ''
        if game['sku'] in all_time_discounted_games:
            all_time_discounted_flag = ' ⚠'
        print(
            f"\tOriginal price: {price['regularPrice']:>6.2f}\t\t-- {price['percentOff']:>6.2f}% off -->\t\tFinal Price: {price['finalPrice']:>6.2f}{all_time_discounted_flag}")

    print('\n⚠ -> Lowest price recorded for game in discount\n')


def insert_info_games(sqlite_connection: SQLiteConnection, game_list: list):
    for game in game_list:
        sql_game = {
            'sku': game['sku'],
            'name': game['name'],
            'url_key': game['urlKey'],
            'price': game['prices']['minimum']['finalPrice'],
            'original_price': game['prices']['minimum']['regularPrice'],
            'discount_percentage': game['prices']['minimum']['percentOff'],
            'discounted': game['prices']['minimum']['discounted'],
            'timestamp_value': int(datetime.now().timestamp())
        }
        sqlite_connection.insert('wishlist_games', sql_game)
    return 0


def get_all_time_discounted_games(sqlite_connection: SQLiteConnection, discounted_games: list) -> list:
    all_discounted_skus = []
    for game in discounted_games:
        query = f"SELECT MIN(price) AS lowest_price FROM wishlist_games WHERE sku = {game['sku']};"
        result = sqlite_connection.select(query)

        lowest_price = None
        if len(result) > 0 and len(result[0]) > 0:
            lowest_price = result[0][0]

        if lowest_price is not None and\
                lowest_price >= game['prices']['minimum']['finalPrice']:
            all_discounted_skus.append(game['sku'])

    return all_discounted_skus
