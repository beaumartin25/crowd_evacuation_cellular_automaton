import solara

from model import Evacuation
from mesa.visualization import (
    Slider,
    SolaraViz,
    make_plot_component,
    make_space_component,
)

def post_process(ax):
    ax.set_aspect("equal")  # Keeps the grid cells square-shaped
    ax.set_xticks([])       # Hides the x-axis ticks
    ax.set_yticks([])       # Hides the y-axis ticks
    ax.set_facecolor("white")  # Sets the background color to white (optional)

def pd_agent_portrayal(agent):
    """
    Portrayal function for rendering PD agents in the visualization.
    """
    return {
        "color": "blue" if agent.move == "C" else "red",
        "marker": "s",  # square marker
        "size": 25,
    }


model_params = {
    "density": Slider("Agent density", 0.8, 0.1, 1.0, 0.1),
    "deflecting_pc": Slider("Fraction starting defect", 0.2, 0.0, 1.0, 0.05),
    "deflector_penalty": Slider("Defector Penalty", 2, 1, 10, 1),
    "width": 40,
    "height": 40,
}

model1 = Evacuation()

plot_component = make_plot_component("Deflecting_Agents")
plot_agents_moved = make_plot_component("Agents_Moved")
plot_exited_count = make_plot_component("Exited_count")

SpaceGraph = make_space_component(
    pd_agent_portrayal, post_process=post_process, draw_grid=False
)

page = SolaraViz(
    model1,
    components=[
        SpaceGraph,
        plot_component,
        plot_agents_moved,
        plot_exited_count,
    ],
    model_params=model_params,
)
page  # noqa