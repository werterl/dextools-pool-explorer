"""
Script for collecting information about new coins from dextools.io
Running the script:

run.py [chain] [logfile]
chain - chain name to choose from (ethereum, bnb, arbitrum, polygon, aptos, solana)
logfile - the name of the file for logging
"""
import sys

from dextools_class import DextoolsClass
from handlers import send_to_telegram_handler, send_to_csv_handler

api_url = 'wss://ws.dextools.io/'
chain = sys.argv[1] if len(sys.argv) > 1 else 'ethereum'
log_file = sys.argv[2] if len(sys.argv) > 2 else None

use = DextoolsClass(api_url=api_url,
                    callback=send_to_telegram_handler,
                    chain=chain,
                    log_file=log_file)
use.run()
