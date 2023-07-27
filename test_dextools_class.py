import unittest
from json import dumps
from unittest.mock import MagicMock, patch
from dextools_class import DextoolsClass


class TestDextoolsClass(unittest.TestCase):
    dextools = None
    mock_callback = None

    def setUp(self) -> None:
        api_url = 'wss://ws.dextools.io/'
        self.mock_callback = MagicMock()
        self.dextools = DextoolsClass(api_url, self.mock_callback)

    def test_on_message_invalid_json(self):
        with patch.object(self.dextools, '_DextoolsClass__log') as mock_log:
            self.dextools._DextoolsClass__on_message(None, 'Invalid JSON')
            mock_log.assert_called_once_with('JSONDecodeError:Invalid JSON', True)

    def test_on_message_event_not_create(self):
        json_message = {
            'result': {
                'status': 'ok',
                'data': {
                    'event': 'update',
                    'pair': {
                        'id': '0x000000',
                    }
                }
            }
        }

        self.dextools._DextoolsClass__on_message(None, dumps(json_message))

        self.mock_callback.assert_not_called()

    def test_on_message_fail_status(self):
        json_message = {
            'result': {
                'status': 'fail',
                'data': {
                    'event': 'create',
                    'pair': {
                        'id': '0x000000',
                    }
                }
            }
        }

        self.dextools._DextoolsClass__on_message(None, dumps(json_message))

        self.mock_callback.assert_not_called()

    def test_on_message_success(self):
        coin_info = {
            'chain': 'ethereum',
            'address': '0x000000',
            'owner': '0x000001',
            'token0': 'BTC',
            'token1': 'USDT',
            'totalSupply': 1000,
            'createdAt': '2022-02-21T09:22:07.820Z',
            'liquidity': 995.5,
            'email': 'mail@test.com',
            'website': 'https//test.com/',
            'twitter': 'https//twitter.com/test',
            'telegram': 'https://t.me/test',
            'description': 'description',
        }

        json_message = {
            'result': {
                'status': 'ok',
                'data': {
                    'event': 'create',
                    'pair': {
                        'info': {
                            'owner': '0x000001',
                            'totalSupply': 1000
                        },
                        'id': '0x000000',
                        'token0': {'symbol': 'BTC'},
                        'token1': {'symbol': 'USDT'},
                        'createdAt': '2022-02-21T09:22:07.820Z',
                        'liquidity': 995.5,
                        'custom': {
                            'info': {
                                'email': 'mail@test.com',
                                'website': 'https//test.com/',
                                'twitter': 'https//twitter.com/test',
                                'telegram': 'https://t.me/test',
                                'description': 'description',
                            }
                        }
                    }
                }
            }
        }

        self.dextools._DextoolsClass__on_message(None, dumps(json_message))

        self.mock_callback.assert_called_once_with(coin_info)


if __name__ == '__main__':
    unittest.main()
