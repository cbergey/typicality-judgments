"""Bots to run the experiment in an automated manner."""
import logging
import requests

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dallinger.bots import BotBase, HighPerformanceBotBase

logger = logging.getLogger(__file__)


class Bot(BotBase):
    """Bot tasks for experiment participation"""

    def participate(self):
        """Click the button."""
        try:
            logger.info("Entering participate method")
            submit = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'submit-response')))
            submit.click()
            return True
        except TimeoutException:
            return False


class HighPerformanceBot(HighPerformanceBotBase):
    """Bot for experiment participation with direct server interaction"""

    def participate(self):
        """Click the button."""
        self.log('Bot player participating.')
        node_id = None
        while True:
            # create node
            url = "{host}/node/{self.participant_id}".format(
                host=self.host,
                self=self
            )
            result = requests.post(url)
            if result.status_code == 500 or result.json()['status'] == 'error':
                self.stochastic_sleep()
                continue

            node_id = result.json.get('node', {}).get('id')

        while node_id:
            # add info
            url = "{host}/info/{node_id}".format(
                host=self.host,
                node_id=node_id
            )
            result = requests.post(url, data={"contents": "Submitted",
                                              "info_type": "Info"})
            if result.status_code == 500 or result.json()['status'] == 'error':
                self.stochastic_sleep()
                continue

            return
