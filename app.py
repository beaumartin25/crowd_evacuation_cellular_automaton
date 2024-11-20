import solara

from model import Evacuation
from mesa.visualization import (
    Slider,
    SolaraViz,
    make_plot_component,
    make_space_component,
)


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
    "deflecting_pc": Slider("Fraction starting deflect", 0.2, 0.0, 1.0, 0.05),
    "width": 20,
    "height": 20,
}

model1 = Evacuation()

plot_component = make_plot_component("Cooperating_Agents")

page = SolaraViz(
    model1,
    components=[
        make_space_component(pd_agent_portrayal),
        plot_component,
    ],
    model_params=model_params,
)
page  # noqa