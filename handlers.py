import configparser
import requests
import csv

config = configparser.ConfigParser()
config.read("config.ini")


def send_to_csv_handler(coin_info: dict[str, any]):
    """Handler for saving coin data to csv file"""
    if config.has_option('csv', 'path'):
        try:
            filename = config['csv']['path']
            with open(filename, 'a', newline='\n') as f:
                # Get the keys for the csv headers
                headers = coin_info.keys()
                # Create a csv writer to work with the dictionary
                writer = csv.DictWriter(f, fieldnames=headers, quoting=csv.QUOTE_ALL)
                # If the file is empty, write the headers as the first row
                if f.tell() == 0:
                    writer.writeheader()
                # Write the row with the coin data
                writer.writerow(coin_info)

        except IOError as e:
            raise Exception('Error writing to file:', str(e))
    else:
        raise ValueError('Section [csv/path] is not filled')


def send_to_telegram_handler(coin_info: dict[str, any]):
    """Handler for sending coin data to Telegram chat using a bot"""
    if config.has_option('telegram', 'bot_token') and config.has_option('telegram', 'chat_id'):
        # Get the bot token and chat id from the config
        bot_token, chat_id = config['telegram']['bot_token'], config['telegram']['chat_id']
        if not bot_token or not chat_id:
            raise ValueError('bot_token or chat_id is empty')

        # Clean fields with None values
        coin_info_clean = {key: value for key, value in coin_info.items() if value is not None}

        # Convert to string for sending to Telegram
        coin_info_text = '\n'.join([f'{key}: {value}' for key, value in coin_info_clean.items()])

        # Make url and request body
        url = 'https://api.telegram.org/bot{}/sendMessage'.format(bot_token)
        data = {'chat_id': chat_id, 'text': coin_info_text}

        # Request and raise an exception, if the response status is not 200
        response = requests.post(url=url, data=data)

        if response.status_code != 200:
            raise Exception('Error request', response.status_code)
    else:
        raise ValueError('Section [telegram] is not filled')
