# Lens Testnet Faucet Bot

A Python script for automating Lens Protocol testnet faucet claims. Demo inspired by [@ChrisYP/nocaptcha-demo](https://github.com/ChrisYP/nocaptcha-demo/blob/master/testnet.lenscan.io.py).

[Lens Faucet](https://testnet.lenscan.io/faucet)

![Lens Faucet Demo](https://github.com/fuhua898/Lens-Faucet/blob/main/faucet.png)

## Features

- Automated faucet claiming for multiple addresses
- Support for IPv6 proxy rotation
- CloudFlare captcha bypass
- Excel file address batch processing
- Configurable start/end address processing
- **Flexible Range**: Choose which addresses to process from your address list

## Requirements

- Python 3.x
- Required Python packages:
  ```bash
  pip install requests
  pip install pynocaptcha
  pip install pandas
  pip install openpyxl
  ```

## Configuration

1. Get your token from [noCaptcha.io](https://goo.su/0np0os1)
2. Configure [Nstproxy](https://goo.su/V64GMH) settings:


## Usage

1. Prepare an Excel file named `Your File Name.xlsx` with an 'Address' column containing wallet addresses
2. Run the script:
   ```bash
   python testnet.lenscan.io.py
   ```
3. Enter the start and end address numbers when prompted
   - For example, if you have 100 addresses and want to process addresses 51-60:
     - Enter start number: 51
     - Enter end number: 60


## Credits

Original demo by [@ChrisYP](https://github.com/ChrisYP/nocaptcha-demo)

## Disclaimer

This tool is for educational purposes only. Please ensure compliance with all relevant terms of service and usage policies. 