#!/usr/bin/env python3

import numpy as np
from mesa import Agent
import logging


class SugarscapeAgent(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.vision = np.random.choice(range(1,7))
        self.metabolism = np.random.choice(range(1,5))
        self.sugar = 10 
        model.grid.position_agent(self)

    def step(self):
        logging.info("Running agent {}...".format(self.unique_id))

    def __str__(self):
        return "Agent {}".format(self.unique_id)

    def __repr__(self):
        return "Agent {}".format(self.unique_id)
