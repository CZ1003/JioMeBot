import urllib
import json
import requests


TOKEN = "387099409:AAFmM5sismztGNYvfUo388Bn9QeEhUUcce8"
#TOKEN = "422679288:AAFmt0jTQIUs-9aZkTMCJ2AhDHWDaToYk3Y"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

class settings:
    def __init__(self):
        pass

    def get_url(self, url):
        response = requests.get(url)
        content = response.content.decode("utf8")
        return content


    def get_json_from_url(self, url):
        content = self.get_url(url)
        js = json.loads(content)
        return js


    def get_updates(self, offset=None):
        url = URL + "getUpdates?timeout=100"
        if offset:
            url += "&offset={}".format(offset)
        js = self.get_json_from_url(url)
        return js


    def get_last_chat_id_and_text(self, updates):
        num_updates = len(updates["result"])
        last_update = num_updates - 1
        text = updates["result"][last_update]["message"]["text"]
        chat_id = updates["result"][last_update]["message"]["chat"]["id"]
        return (text, chat_id)


    def send_message(self, text, chat_id, reply_markup=None):
        text = urllib.parse.quote_plus(text)
        url = URL + "sendMessage?text={}&chat_id={}&parse_mode=HTML".format(text, chat_id)
        if reply_markup:
            url += "&reply_markup={}".format(reply_markup)
        self.get_url(url)


    def get_last_update_id(self, updates):
        update_ids = []
        for update in updates["result"]:
            update_ids.append(int(update["update_id"]))
        return max(update_ids)


    def build_keyboard(self, code):
        if code == 1:
            keyboard = [[item] for item in ['Food Hitchee', 'Food Hitcher', 'What is this?']]
            reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
        elif code == 2:
            keyboard = [[item] for item in ['Yes!', 'No!']]
            reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
        elif code == 3:
            keyboard = [[item] for item in ['Place an order', 'View placed orders']]
            reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
        elif code == 4:
            keyboard = [[item] for item in ['View all orders', 'View confirmed orders']]
            reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
        return json.dumps(reply_markup)
