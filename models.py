from dallinger.nodes import Source
import random


class adjectivenounsource(Source):
    """A Source that reads in a random story from a file and transmits it."""

    __mapper_args__ = {"polymorphic_identity": "war_of_the_ghosts_source"}

    def _contents(self):
        """Define the contents of new Infos.

        transmit() -> _what() -> create_information() -> _contents().
        """
        stories = [
            ["blue whale red strawberry green grass red sky wooden table purple pig little boy tall building thin reed tasty salad"],
            ["red sky wooden table purple pig little boy tall building thin reed blue whale red strawberry green grass round ball"],
            ["little boy tall building thin reed tall building green fly blue whale small mouse round ball tasty salad red strawberry"],
            ["small mouse round ball tasty salad little boy tall building thin reed tall building thin reed blue whale wooden table"]
        ]
        story = stories[self.network_id-1]
        print(story)
        #with open("static/stimuli/{}".format(story), "r") as f:
         #   return f.read()
        return story
