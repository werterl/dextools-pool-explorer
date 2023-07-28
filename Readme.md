# Dextools Pool Explorer Parser
Collecting information about new coins from the website https://www.dextools.io/

## Description
The Dextools Pool Explorer Parser is a script designed to collect information about new coins from the website [Dextools](https://www.dextools.io/).   
It enables users to monitor the appearance of new coins on Dextools and take action by either sending the information or saving it for later use.

## Usage
1. Specify the handler in the file run.py (callback=[send_to_csv_handler|send_to_telegram_handler]):
    - send_to_csv_handler: for saving to a CSV file.
    - send_to_telegram_handler: for sending to a Telegram chat using a bot.

2. Update the configuration file by adding the filename for saving or the necessary data for Telegram.
3. Run `run.py` to start
```bash
run.py [chain] [logfile]
```

`[chain]`:Choose one of the following chain names: ethereum, bnb, arbitrum, polygon, aptos, solana (default: ethereum)  
`[logfile]`:Specify the name of the log file for storing information (default: disabled).