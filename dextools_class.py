import websocket
import logging
import json
from typing import Callable, Dict, Any


class DextoolsClass:
    # List of available chains. Can be expanded with other chains
    CHAINS = {
        'ethereum': {'chain': 'ether', 'channel': 'uni:pools'},
        'bnb': {'chain': 'bsc', 'channel': 'bsc:pools'},
        'arbitrum': {'chain': 'arbitrum', 'channel': 'arbitrum:pools'},
        'polygon': {'chain': 'polygon', 'channel': 'polygon:pools'},
        'aptos': {'chain': 'aptos', 'channel': 'aptos:pools'},
        'solana': {'chain': 'solana', 'channel': 'solana:pools'},
    }
    _chain = None
    _callback = None
    _client = None
    _log_file: str = None
    # Message for subscribing to the stream
    _init_message: str = '{{"jsonrpc":"2.0","method":"subscribe","params":{{"chain":"{}","channel":"{}"}}}}'

    def __log(self, message: str, is_error: bool = False):
        if self._log_file is not None:
            logging.error(message) if is_error else logging.info(message)

    def __on_message(self, _, message: str):
        """Analyze the message received from the server and call the callback function"""
        try:
            _json = json.loads(message)
            result = _json.get('result', {})
            data = result.get('data', {})

            status = result.get('status')
            # For suitable messages, the data type is an object
            event = data.get('event') if isinstance(data, dict) else ''

            if status == 'ok' and event == 'create':
                pair = data.get('pair', {})
                # Contains owner address and supply
                info = pair.get('info', {})
                # Contains information about social networks, email address and website url
                custom = pair.get('custom', {}).get('info', {})
                # Information about the coin pair (symbols)
                token0 = pair.get('token0', {})
                token1 = pair.get('token1', {})

                coin_info = {
                    'chain': self._chain,
                    'address': pair.get('id'),
                    'owner': info.get('owner'),
                    'token0': token0.get('symbol'),
                    'token1': token1.get('symbol'),
                    'totalSupply': info.get('totalSupply'),
                    'createdAt': pair.get('createdAt'),
                    'liquidity': pair.get('liquidity'),
                    'email': custom.get('email'),
                    'website': custom.get('website'),
                    'twitter': custom.get('twitter'),
                    'telegram': custom.get('telegram'),
                    'description': custom.get('description')
                }

                # If the address was not obtained for some reason, the callback function will not be called
                if coin_info['address']:
                    try:
                        self._callback(coin_info)
                    except Exception as e:
                        self.__log(str(e), True)

        except json.JSONDecodeError:
            self.__log('JSONDecodeError:' + message, True)

    def __on_close(self, _, code, msg):
        self.__log('Connection closed: ' + str(code) + ':' + str(msg))

    def __on_open(self, client):
        self.__log('Connection opened')
        # Subscribe to the stream
        client.send(self._init_message)

    def __on_error(self, _, error):
        self.__log('Client error: ' + str(error), True)

    def __init__(self, api_url: str, callback: Callable[[Dict[str, Any]], None],
                 chain: str = 'ethereum', log_file: str = None):
        # Setting up a handler that will be called after receiving the information
        self._callback = callback
        # Setting up logging if a log file name is provided
        if log_file is not None:
            self._log_file = log_file
            logging.basicConfig(filename=log_file,
                                level=logging.INFO,
                                format='%(asctime)s - %(levelname)s - %(message)s')

        if chain not in self.CHAINS:
            raise ValueError('Chain not found')

        current_chain = self.CHAINS[chain]
        self._chain = chain
        # Set parameters in the initialization message for the listener
        self._init_message = self._init_message.format(current_chain['chain'], current_chain['channel'])
        # Create a websocket client and set event handlers
        self._client = websocket.WebSocketApp(api_url,
                                              on_message=self.__on_message,
                                              on_open=self.__on_open,
                                              on_error=self.__on_error,
                                              on_close=self.__on_close)
        websocket.enableTrace(False)

    def run(self):
        """Function to start listening to the stream"""
        self._client.run_forever()
