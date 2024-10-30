import requests
import json
import time
import threading
from requests.exceptions import RequestException, HTTPError, Timeout
from functools import lru_cache
import os
import secret.token as token

# Get Tron API key from environment variable or prompt user if not set
# TRON_SCAN_API_KEY = os.getenv('TRON_SCAN_API_KEY', 'YOUR_API_KEY')
TRON_SCAN_API_KEY = token.TRON_SCAN_API_KEY
TIMEOUT = 23  # Timeout for API requests in seconds
MAX_THREADS = 1  # Maximum number of threads for parallel search


# Cache transactions to minimize API calls for the same address
@lru_cache(maxsize=None)
def get_transactions(address, start=0, end=99999999, page_num=1, limit=100, order='asc', max_attempts=3, pause=1):
    """
    Fetch TRON transactions for a given address from the TronScan API.

    :param address: TRON address to query
    :param start: Start time for transaction history
    :param end: End time for transaction history
    :param page_num: Page number for paginated results
    :param limit: Number of transactions per page
    :param order: Sorting order ('asc' or 'desc')
    :param max_attempts: Number of retry attempts in case of failure
    :param pause: Delay between retry attempts in seconds
    :return: List of transactions or empty list if unsuccessful
    """
    url = (f"https://apilist.tronscan.org/api/transaction?address={address}&sort={order}"
           f"&start={start}&end={end}&page={page_num}&limit={limit}")

    for attempt in range(max_attempts):
        try:
            response = requests.get(url, timeout=TIMEOUT, headers={'TRON-PRO-API-KEY': f'{TRON_SCAN_API_KEY}'})
            print(response.text)
            response.raise_for_status()  # Raise an error for bad HTTP responses
            data = response.json()

            if 'data' in data:  # Success case for TronScan API
                return data.get('data', [])
            else:  # TronScan API error response
                print(f"API error: {data.get('error')}")
                return []
        except (RequestException, HTTPError, Timeout) as e:
            print(f"Request attempt {attempt + 1}/{max_attempts} failed: {str(e)}")
            if attempt < max_attempts - 1:
                time.sleep(pause)
            else:
                return []


def find_connection(address1, address2, max_depth=3, current_depth=1, log=None):
    """
    Recursively find a transaction path between two Ethereum addresses.

    :param address1: Starting Ethereum address
    :param address2: Target Ethereum address
    :param max_depth: Maximum depth for recursive search
    :param current_depth: Current depth of the search
    :param log: List to log progress (optional)
    :return: True if a connection is found, False otherwise
    """
    if current_depth > max_depth:
        return False

    log_and_print(f"Depth {current_depth}: Checking transactions for {address1}", log)
    transactions = get_transactions(address1)

    log_and_print(f"Depth {current_depth}: {len(transactions)} transactions found for {address1}", log)

    for tx in transactions:
        from_address = tx.get('ownerAddress', '').lower()
        to_address = tx.get('toAddress', '').lower()
        tx_hash = tx.get('hash', '')

        log_and_print(f"Depth {current_depth}: Checking tx {tx_hash} from {from_address} to {to_address}", log)

        if to_address == address2.lower():
            log_and_print(f"Depth {current_depth}: Direct connection found in tx {tx_hash}", log)
            return True
        elif current_depth < max_depth and find_connection(to_address, address2, max_depth, current_depth + 1, log):
            log_and_print(f"Depth {current_depth}: Indirect connection found via {to_address}", log)
            return True

    return False


def log_and_print(message, log=None):
    """
    Log a message with a timestamp and optionally append it to a list.

    :param message: Message to be logged
    :param log: List to store log messages (optional)
    """
    timestamped_message = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}"
    print(timestamped_message)
    if log is not None:
        log.append(timestamped_message)


def main(address1, address2, max_threads=MAX_THREADS, log_file='connection_log.txt'):
    """
    Main function to orchestrate the search for a connection between two Ethereum addresses.

    :param address1: Starting Ethereum address
    :param address2: Target Ethereum address
    :param max_threads: Number of threads for parallel search
    :param log_file: Path to save the log output
    """
    log = []
    log_and_print(f"Starting connection search between {address1} and {address2}", log)

    connection_found = threading.Event()

    def check_connection():
        if find_connection(address1, address2, log=log):
            connection_found.set()

    # Create threads for parallel search
    threads = []
    for _ in range(max_threads):
        thread = threading.Thread(target=check_connection)
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    if connection_found.is_set():
        log_and_print("Connection found!", log)
    else:
        log_and_print("No connection found.", log)

    # Save logs to a file
    with open(log_file, 'w') as f:
        f.write("\n".join(log))


if __name__ == "__main__":
    # Example addresses to search for a connection between
    address2 = "TCY4Z6qhjbEoTyykCA9kv2ENkVJnFcy4vm"
    address1 = 'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t'

    main(address1, address2)
