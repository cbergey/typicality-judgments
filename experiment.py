""" experiment to elicit typicality judgments about noun-adjective pairs"""

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
        """Call the same function in the super (see experiments.py in dallinger).

        A few properties are then overwritten.

        Finally, setup() is called.
        """
        super(typicalityjudgments, self).__init__(session)
        from . import models  # Import at runtime to avoid SQLAlchemy warnings

        self.models = models
        self.experiment_repeats = 4
        self.initial_recruitment_size = 1
        if session:
            self.setup()

    def configure(self):
        config = get_config()
        self.num_participants = config.get("num_participants")

    def setup(self):
        """Setup the networks.

        Setup only does stuff if there are no networks, this is so it only
        runs once at the start of the experiment. It first calls the same
        function in the super (see experiments.py in dallinger). Then it adds a
        source to each network.
        """
        if not self.networks():
            super(typicalityjudgments, self).setup()
            for net in self.networks():
                self.models.adjectivenounsource(network=net)

    def create_network(self):
        """Return a new network."""
        return Burst(max_size = 3)

    def add_node_to_network(self, node, network):
        """Add node to the chain and receive transmissions."""
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
        """Recruit one participant at a time until all networks are full."""
        if self.networks(full=False):
            self.recruiter.recruit(n=1)
        else:
            self.recruiter.close_recruitment()


class Bot(BotBase):
    """Bot tasks for experiment participation"""

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

    def transform_text(self, text):
        """Experimenter decides how to simulate participant response"""
        return "Some transformation...and %s" % text
