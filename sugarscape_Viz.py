
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.ModularVisualization import ModularServer

from sugarscape import Sugarscape
from agent import SugarscapeAgent

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Color": "black",
                 "Filled": "true",
                 "Layer": 0,
                 "r": .7}
    return portrayal


if __name__ == "__main__":
    N = 10

    # The width and height should really be read from the scape_file.
    grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

    server = ModularServer(Sugarscape, [grid],
        "Sugarscape",
        { "N":N, "scape_filename":"fake.csv",
        "agent_class":SugarscapeAgent })
    server.port = 8081
    server.launch()
