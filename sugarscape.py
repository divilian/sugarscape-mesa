#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mesa import Agent, Model
from mesa.space import SingleGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner
import logging
import time
import subprocess
import sys
import glob

from agent import SugarscapeAgent, EnvSquare

logging.basicConfig(level=logging.WARNING)

def compute_gini(model):
    w = sorted([a.wealth for a in model.schedule.agents])
    N = model.num_agents
    B = sum(wi * (N-i) for i,wi in enumerate(w)) / (N*sum(w))
    return (1 + (1/N) - 2*B)


class Sugarscape(Model):

    def __init__(self, N, agent_class, raw_scape_array, growback_rate=np.Inf,
            replace=True):
        self.num_agents = N
        self.growback_rate = growback_rate
        self.replace = replace
        self.schedule = RandomActivation(self)
        self.num_steps = 0
        self.scape = self._load_scape(raw_scape_array)
        self.width = self.scape.shape[0]
        self.height = self.scape.shape[1]
        self.grid = SingleGrid(self.width, self.height, False)
        for i in range(self.num_agents):
            a = agent_class(i, self)
            self.schedule.add(a)
        self.running = True   # could set this to stop prematurely

    def _load_scape(self, raw_scape_array):
        """
        The raw_scape_array should be a NumPy array of ints, each element
        representing the initial, and max capacity, of a sugarscape cell.
        """
        scape = np.empty(raw_scape_array.shape,dtype=EnvSquare)
        for row in range(scape.shape[0]):
            for col in range(scape.shape[1]):
                scape[row][col] = EnvSquare(raw_scape_array[row,col],
                    raw_scape_array[row,col])
        print(scape.shape)
        return scape


    def step(self):
        self.num_steps += 1
        logging.info("Iteration {}...".format(self.num_steps))
        #self.datacollector.collect(self)
        self.schedule.step()

        # Replacement rule G_alpha (p.23)
        self._growback(self.growback_rate)

    def _growback(self, growback_rate):
        for row in range(self.scape.shape[0]):
            for col in range(self.scape.shape[1]):
                sq = self.scape[row,col]
                if sq.curr < sq.max:
                    self.scape[row,col] = EnvSquare(
                        min(sq.curr + growback_rate, sq.max), sq.max)

    def run(self, num_steps=50):
        for _ in range(num_steps):
            self.step()



if __name__ == "__main__":

    if len(sys.argv) <= 1:
        print("Usage: sugarscape.py single|batch.")
        sys.exit()

    if sys.argv[1] == "single":

        # Single simulation run.
        m = Sugarscape(10, SugarscapeAgent, "50x50.csv")
        m.run(5)

    else:

        # Batch simulation run.
        print("Batch not implemented yet.")
