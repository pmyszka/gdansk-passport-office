import logging
import requests
import schedule
import sys
import time
import urllib3

from notifiers import PushoverNotifier

logger = logging.getLogger(__name__)


class GdanskPassportOffice:
  base_url = 'https://rezerwacja.gdansk.uw.gov.pl:8445/qmaticwebbooking/rest/schedule/branches/{0}/dates;servicePublicId={1};customSlotLength={2}'
  branch_id = '1cf1e3e60eeb96dae2bb572487249bd48cc5bed0024960eaee0c893ce4918569'
  service_id = '4fe2df1ac02036b7096beb9b80b8e0e8924c3c282eb992fc83b5a3977ddd20b1'

  slot_adult_with_child = '15'
  slot_adult = '10'

  def __init__(self, slot, notifier):
    self.url = self.base_url.format(self.branch_id, self.service_id, slot)
    self.notifier = notifier

  def list_appointments(self):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = requests.get(self.url, verify=False)
    if response.status_code != 200:
      logger.error(
        "Failed to contact the APIs: HTTP {0}".format(response.status_code))
      sys.exit(1)

    if response.text != '[]':
      self.notifier.notify("Available slots: {0}".format(response.text))
      logger.info("Response: {0}".format(response.text))

  def scan_for_appointments(self):
    schedule.every(5).seconds.do(self.list_appointments)
    while True:
      schedule.run_pending()
      time.sleep(1)


def main():
  logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

  slot = GdanskPassportOffice.slot_adult_with_child

  GdanskPassportOffice(slot, PushoverNotifier()).scan_for_appointments()


if __name__ == '__main__':
  main()
