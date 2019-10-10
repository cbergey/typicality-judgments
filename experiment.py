""" experiment to elicit typicality judgments about noun-adjective pairs """

import logging

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dallinger.bots import BotBase
from dallinger.config import get_config
from dallinger.networks import Burst
from dallinger.experiment import Experiment


logger = logging.getLogger(__file__)


def extra_parameters():
    config = get_config()
    config.register("num_participants", int)


class typicalityjudgments(Experiment):
    """Define the structure of the experiment."""

    def __init__(self, session=None):
        """
        calls init in super and overwrites models, repeats, recruitment size
        """
        super(typicalityjudgments, self).__init__(session)
        from . import models 

        self.models = models
        self.experiment_repeats = 111
        self.initial_recruitment_size = 40
        if session:
            self.setup()

    def configure(self):
        config = get_config()
        self.num_participants = config.get("num_participants")

    def setup(self):
        """
        set up networks
        """
        if not self.networks():
            super(typicalityjudgments, self).setup()
            for net in self.networks():
                self.models.adjectivenounsource(network=net)

    def create_network(self):
        """
        return a new burst network. 
        this network has a central node which distributes the stimuli; 
        participant nodes attach to it and only receive info from it.

        max_size is the number of judgments per item + 1.
        """
        return Burst(max_size = 5)

    def add_node_to_network(self, node, network):
        """add node to the burst and get transmission (stimuli) from center of burst"""
        network.add_node(node)
        parents = node.neighbors(direction="from")
        if len(parents):
            parent = parents[0]
            parent.transmit()
        node.receive()

    def get_network_for_participant(self, participant):
        
        key = participant.id

        for network in self.networks():
            if network.nodes(participant_id = participant.id):
                return None

        networks_with_space = (
            self.networks(full=False)
        )

        if not len(networks_with_space):
            self.log("No networks available, returning None", key)
            return None

        chosen_network = self.choose_network(networks_with_space, participant)
        self.log(
            "Assigning participant to experiment network {}".format(
                chosen_network.id
            ),
            key,
        )
        return chosen_network

    def recruit(self):
        """recruit one at a time"""
        if self.networks(full=False):
            self.recruiter.recruit(n=1)
        else:
            self.recruiter.close_recruitment()
'''
    def attention_check(self, participant):
        node = participant.nodes()[0]
        val = int(node.infos()[-1].contents)
        atn = node.infos()[-1].property2
        self.log(val)
        self.log(atn)
        self.log(val == 5)
        return (val == 5)
'''


class Bot(BotBase):
    """we're not using bots yet, but this is a mockup of what they might do"""

    def participate(self):
        """Finish reading and send text"""
        try:
            logger.info("Entering participate method")
            ready = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "finish-reading"))
            )
            stimulus = self.driver.find_element_by_id("stimulus")
            story = stimulus.find_element_by_id("story")
            logger.info("Stimulus text:")
            logger.info(story)
            ready.click()
            submit = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "submit-response"))
            )
            textarea = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "reproduction"))
            )
            textarea.clear()
            text = story 
            logger.info("Transformed text:")
            logger.info(text)
            textarea.send_keys(text)
            submit.click()
            return True
        except TimeoutException:
            return False
