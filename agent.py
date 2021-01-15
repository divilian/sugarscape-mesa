#!/usr/bin/env python3

import numpy as np
from mesa import Agent
import logging
from collections import namedtuple

EnvSquare = namedtuple('EnvSquare', 'curr max')

class SugarscapeAgent(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.vision = np.random.choice(range(1,7))
        self.metabolism = np.random.choice(range(1,5))
        self.sugar = 10 
        model.grid.position_agent(self)

    def step(self):
        logging.info("Running agent {}...".format(self.unique_id))
        dest = self._visible_neighbor_with_most_sugar()
        logging.info("Move from {} to {}".format(self.pos, dest))
        self.model.grid.move_agent(self, dest)
        self.sugar += self.model.scape[dest].curr
        self.model.scape[dest] = EnvSquare(0, self.model.scape[dest].max)

    def _visible_neighbor_with_most_sugar(self):
        dest = (np.random.choice(range(self.model.grid.width)),
            np.random.choice(range(self.model.grid.width)))
        while not self.model.grid.is_cell_empty(dest):
            dest = (np.random.choice(range(self.model.grid.width)),
                np.random.choice(range(self.model.grid.width)))
        return dest

    def __str__(self):
        return "Agent {}".format(self.unique_id)

    def __repr__(self):
        return "Agent {}".format(self.unique_id)
