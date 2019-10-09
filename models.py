from dallinger.nodes import Source
import random
import csv 
numtrials = 20

class adjectivenounsource(Source):
    """A Source that reads in a random story from a file and transmits it."""

    __mapper_args__ = {"polymorphic_identity": "adjective_noun_source"}

    def _contents(self):
        """Define the contents of new Infos.

        transmit() -> _what() -> create_information() -> _contents().
        """
        allstims = list()
        with open("static/stimuli/pairs_for_turk.csv") as f:  
            reader = csv.reader(f)
            i = 0
            stims = list()
            for row in reader:
                if row[0] == "adj":
                    continue
                if i == numtrials:
                    allstims.append(stims)
                    stims = list()
                    i = 0
                stims.append(row)
                i += 1

        thesestims = allstims[self.network_id-1]
        return thesestims
