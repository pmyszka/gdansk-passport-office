import requests
from dotenv import dotenv_values


class PushoverNotifier:
  url = 'https://api.pushover.net/1/messages.json'

  def __init__(self):
    config = dotenv_values()
    self.token = config['PUSHOVER_TOKEN']
    self.user = config['PUSHOVER_USER']

  def notify(self, payload):
    requests.post(self.url, data={'token': self.token, 'user': self.user,
                                  'message': payload})
