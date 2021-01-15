
import numpy as np
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.ModularVisualization import ModularServer

from sugarscape import Sugarscape
from agent import SugarscapeAgent, EnvSquare

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Color": "black",
                 "Filled": "true",
                 "Layer": 1,
                 "r": agent.sugar / 100}
    return portrayal


class SugarscapeGrid(CanvasGrid):
        
    def render(self, model):
        scape = model.scape
        grid_state = super().render(model)
        portrayal_template = {
            "Shape":"rect",
            "Filled":"true",
            "Layer": 0,
            "w":1,
            "h":1,
        }
        
        for x in range(model.grid.width):
            for y in range(model.grid.height):
                portrayal = portrayal_template.copy()
                portrayal["x"] = x
                portrayal["y"] = y
                hex_str = self._compute_hex_str(scape[x,y].curr)
                portrayal["Color"] = "#ffff{}".format(hex_str,hex_str)
                grid_state[portrayal["Layer"]].append(portrayal)

        return grid_state

    def _compute_hex_str(self, i):
        return hex((255 - (i * 50) % 255))[2:].zfill(2)

if __name__ == "__main__":

    N = 10

    """
    A scape file is a .csv file with integers representing the max sugar
    capacity of each sugarscape cell.
    """
    raw_scape_array = np.loadtxt("50x50.csv",delimiter=",",dtype=int)

    grid = SugarscapeGrid(agent_portrayal, raw_scape_array.shape[0],
        raw_scape_array.shape[1], 500, 500)

    server = ModularServer(Sugarscape, [grid],
        "Sugarscape",
        { "N":N, "raw_scape_array":raw_scape_array,
        "agent_class":SugarscapeAgent })
    server.port = 8081
    server.launch()
