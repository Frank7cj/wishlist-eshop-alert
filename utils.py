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


def get_discounted_games(games_info: dict) -> list:
    products = games_info['data']['products']

    discounted_games = []

    for game in products:
        price = game['prices']['minimum']
        if price['discounted']:
            discounted_games.append(game)

    return discounted_games


def print_discounted_games(discounted_games: list, locale_url: str):
    print('-'*50)
    print("! Alert Nintendo eShop game(s) in discount")
    for game in discounted_games:
        print(
            f"{game['name']} | https://www.nintendo.com/{locale_url}/store/products/{game['urlKey']}")
        price = game['prices']['minimum']
        print(
            f"\tOriginal price: {price['regularPrice']:>6.2f}\t\t-- {price['percentOff']:>6.2f}% off -->\t\tFinal Price: {price['finalPrice']:>6.2f}")
