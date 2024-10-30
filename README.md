# Wallet Connection Detector

This Python script detects a connection between two wallet addresses using APIs such as Etherscan for Ethereum or TronScan for TRON. It logs the detailed process and results to both the console and a log file.

## Features

- Retrieve transactions of Ethereum or TRON addresses.
- Recursively search for connections between two addresses.
- Log the process and results to the console and a file.

## Requirements

- Python 3.8+
- Requests library

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/gonchik/wallet-connection-detector.git
    cd wallet-connection-detector
    ```

2. Install the required Python package:

    ```sh
    pip install requests
    ```

## Usage

### Ethereum

1. Get an Etherscan API key by registering on the [Etherscan website](https://etherscan.io/register).

2. Replace the placeholder `YOUR_API_KEY` in the script with your actual Etherscan API key.

3. Replace `0xAddress1` and `0xAddress2` in the script with the Ethereum addresses you want to check.

### TRON

For TRON, ensure you have access to a TRON blockchain explorer API if needed (like TronScan).

3. Replace `TRON_ADDRESS1` and `TRON_ADDRESS2` in the script with the TRON addresses you want to check.

4. Run the script:

    ```sh
    python find_connection.py
    ```

### Example

Here's an example of how to set up the script:

```python
if __name__ == "__main__":
    # Replace these with the Ethereum addresses you want to check
    address1 = "0xasddasd"
    address2 = "0xsads"
    main(address1, address2)
```

## Output

The script will print the progress to the console and save the log to `connection_log.txt`.

### Sample Console Output

```
Depth 2: 0 transactions found for tr7nhqjekqxgtci8q8zy4pl8otszgjlj6t
Depth 1: Checking tx 0e7a2d7350387e81ff075f5826497d2c8017d16c89acbeb5960c024ebe1fc8e1 from tu4veruvzwllksfv9bnw12ejtpvnr7pvaa to tr7nhqjekqxgtci8q8zy4pl8otszgjlj6t
Depth 2: Checking transactions for tr7nhqjekqxgtci8q8zy4pl8otszgjlj6t
Depth 2: 0 transactions found for tr7nhqjekqxgtci8q8zy4pl8otszgjlj6t
Depth 1: Checking tx 6d39a4c5e97888f7c2978d280b690db6b8708a636fb62ae5875001588859525a from tt7bepbquxl6r2xlw5gyjjww27tkecry7f to tr7nhqjekqxgtci8q8zy4pl8otszgjlj6t
Depth 2: Checking transactions for tr7nhqjekqxgtci8q8zy4pl8otszgjlj6t
Depth 2: 0 transactions found for tr7nhqjekqxgtci8q8zy4pl8otszgjlj6t
No connection found.
```

### Sample Log File (`connection_log.txt`)

```

...
No connection found.
```

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the Apache 2 License - see the [LICENSE](LICENSE) file for details.