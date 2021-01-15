#!/usr/bin/env python3

import numpy as np
from mesa import Agent
import logging
from collections import namedtuple
import operator

EnvSquare = namedtuple('EnvSquare', 'curr max')

class SugarscapeAgent(Agent):

    max_id = 0

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        SugarscapeAgent.max_id = max(SugarscapeAgent.max_id, unique_id)
        self.vision = np.random.choice(range(1,7))
        self.metabolism = np.random.choice(range(1,5))
        self.max_age = np.random.choice(range(60,100))
        self.age = 0
        self.sugar = np.random.choice(range(5,25))
        self.color = "red"
        model.grid.position_agent(self)

    def step(self):
        logging.info("Running agent {}...".format(self.unique_id))

        # Agent movement rule M (p.25)
        dest = self._visible_neighbor_with_most_sugar()
        logging.info("Move from {} to {}".format(self.pos, dest))
        self.model.grid.move_agent(self, dest)
        self.sugar += self.model.scape[dest].curr
        self.model.scape[dest] = EnvSquare(0, self.model.scape[dest].max)
        self.sugar -= self.metabolism
        self.age += 1
        if self.age > self.max_age  or  self.sugar < 0:
            self.die()

    def die(self):
        logging.info("{} died!".format(self))
        self.model.schedule.remove(self)
        self.model.grid.remove_agent(self)

        # Replacement rule R_a,b (p.32)
        replacement = SugarscapeAgent(SugarscapeAgent.max_id + 1, self.model)
        replacement.color = "green"
        self.model.schedule.add(replacement)

    def _visible_neighbor_with_most_sugar(self):
        nei = { n:self.model.scape[n][0] 
            for n in self.model.grid.iter_neighborhood(self.pos,
                moore=False, include_center=False, radius=self.vision) 
            if (n[0] == self.pos[0] or n[1] == self.pos[1]) 
                and self.model.grid.is_cell_empty(n) }
        if len(nei) == 0:
            return self.pos
        return max(nei.items(), key=operator.itemgetter(1))[0]

    def __str__(self):
        return "Agent {}".format(self.unique_id)

    def __repr__(self):
        return "Agent {}".format(self.unique_id)
