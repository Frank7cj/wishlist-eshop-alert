# Alert eShop Wishlist

A Python-based tool to monitor and alert users about discounted games on the Nintendo eShop. This tool fetches game information from the Nintendo API, processes the data, and provides insights into discounted games, including historical lowest prices.

## Features

- Fetch game information from the Nintendo eShop API.
- Identify discounted games from a wishlist.
- Track historical lowest prices for games using SQLite.
- Export game data to JSON files.
- Command-line interface for easy configuration and usage.

## Requirements

- Python 3.8+
- Dependencies listed in [`requirements.txt`](requirements.txt)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Frank7cj/wishlist-eshop-alert.git
   cd wishlist-eshop-alert
   ```

2. Create a virtual environment and activate it:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command-Line Arguments

Run the script using the following command:

```bash
python main.py --wishlist_url <WISHLIST_URL> --request_config <CONFIG_FILE> [--sqlite_path <SQLITE_FILE>] [--json_export <1|0>]
```

#### Arguments

- `--wishlist_url` (required): The URL of your Nintendo eShop wishlist (shared from <https://www.nintendo.com/wish-list/>).
- `--request_config` (required): Path to a JSON configuration file for API requests (e.g., [`template_config.jsonc`](template_config.jsonc)).
- `--sqlite_path` (optional): Path to an SQLite database file for storing game data.
- `--json_export` (optional): Export game data to a JSON file (1 = Yes, 0 = No).

### Example

```bash
python main.py --wishlist_url "https://www.nintendo.com/wish-list/..." \
               --request_config template_config.jsonc \
               --sqlite_path wishlist_games.sqlite \
               --json_export 1
```

## Configuration

The API request configuration is stored in a JSON file (e.g., [`template_config.jsonc`](template_config.jsonc)). Update the `sha256Hash` field in the `extensions` section with the appropriate hash for querying game information.

### Example Configuration

```jsonc
{
  "api_endpoint": "https://graph.nintendo.com/",
  "extensions": {
    "persistedQuery": {
      "version": 1,
      "sha256Hash": "your_sha256_hash_here"
    }
  },
  "headers": {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "apollographql-client-name": "ncom",
    "apollographql-client-version": "1.0.0",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "origin": "https://www.nintendo.com",
    "pragma": "no-cache",
    "referer": "https://www.nintendo.com/"
  }
}
```

## Database

The tool uses SQLite to store game data. The database schema is defined in the `NINTENDO_GAME_COLUMNS` dictionary in [`main.py`](main.py). The table `wishlist_games` is created if it does not already exist.

### Schema

- `sku`: Game SKU (unique identifier).
- `name`: Game name.
- `url_key`: URL key for the game.
- `price`: Current discounted price.
- `original_price`: Original price.
- `discount_percentage`: Discount percentage.
- `discounted`: Whether the game is currently discounted.
- `timestamp_value`: Timestamp of the record.

## Output

- **Console Output**: Displays discounted games with their details, including historical lowest prices.
- **JSON Export**: If enabled, saves game data to a JSON file with a timestamped filename.
- **SQLite Database**: Stores game data for historical price tracking.

## Development

### Code Structure

- [`main.py`](main.py): Entry point for the application.
- [`utils.py`](utils.py): Utility functions for processing game data.
- [`sqlite_connection.py`](sqlite_connection.py): SQLite database connection and operations.
- [`template_config.jsonc`](template_config.jsonc): Template for API request configuration.

### Testing

To test the application, ensure you have a valid wishlist URL and API configuration. Run the script with the appropriate arguments and verify the output.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Nintendo eShop API for providing game data.
- Python community for the libraries used in this project.
