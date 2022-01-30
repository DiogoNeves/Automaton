"""

Implementation of a cellular automaton to generate a simple terrain-like structure, from noise.

The implementation includes 3 main stages:
1. Generate initial state
2. Run the CA rule for a few iterations
3. Display the results

This implementations keeps all the intermediate states so that they can be later displayed or analysed.
Results displayed include the full sequence of states and a plot of the number of live cells over time.

---
I tried to keep it short and simple too and hopefully most functions have self-evident intentions.
Some tests are provided in Replit.
No attempts were made at optimising the code.

This program intends to serve as a fun night of code and a framework to study the behaviour of simple CA.

"""

from typing import Callable, List
from scipy.ndimage import filters
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

Grid = List[List[bool]]
GridGenerator = Callable[[], Grid]
Rule = Callable[[Grid], bool]


"""
== Generators ==
"""

def create_noisy_grid(dimension: int, density: float) -> Grid:
    """
  Create a simple noise NxN grid.

  Arguments:
    - dimension: dimension of the side of the grid (square).
    - density: density of live cells to generate.
  """
    return np.random.choice([False, True],
                            size=(dimension, dimension),
                            p=[1 - density, density])


"""
== Rules ==
"""


def mostly_walls(window: Grid) -> bool:
    """Decide if the current cell should be alive, based on how many live cells exist in the window."""
    return np.sum(window) >= 5


def sides(window: Grid) -> bool:
    """Decide if the current cell should be alive, based on the side neighbours."""
    diagonal = [[True, False, True], [False, False, False],
                [True, False, True]]
    return np.sum(np.logical_and(window, diagonal)) >= 1


"""
== Execution ==
"""


def run_automaton(grid: Grid, rule: Rule, iterations: int) -> Grid:
    """Run the automaton for some number of iterations."""
    def rule_shape_wrapper(window: Grid) -> bool:
        # This is mostly done to avoid complexity in some rule implementations
        window = np.reshape(window, (3, 3))
        return rule(window)

    states = [grid]
    for _ in range(iterations):
        # Slides a 3x3 window over the grid
        new_state = filters.generic_filter(states[-1],
                                           rule_shape_wrapper,
                                           size=(3, 3),
                                           mode="constant",
                                           cval=False)
        states.append(new_state)

    return states


def render_animation(states, figure, subplot):
  # Show initial state first
  subplot.imshow(states[-1], interpolation="None")
  
  images = []
  for state in states:
    plotted_image = subplot.imshow(state, interpolation="none", animated=True)
    images.append([plotted_image])
  
  return animation.ArtistAnimation(figure, images, interval=180, blit=True, repeat_delay=2000)


def render_analysis(states, figure, subplot):
  subplot.title.set_text('Live Cells')
  live_cell_count = np.fromiter((np.sum(state) for state in states), int)
  return subplot.plot(range(len(states)), live_cell_count)


def render_result(states):
    """Show the animated state transitions and plot live cells over time."""
    f = plt.figure("Cellular Automaton")

    subplots = f.subplots(2)
    state_animation = render_animation(states, f, subplots[0])
    state_analysis = render_analysis(states, f, subplots[1])

    # Warning: This code isn't portable! I focused on getting it to work with Replit
    figManager = plt.get_current_fig_manager()
    figManager.resize(*figManager.window.maxsize())

    plt.show()


def main():
    initial_state = create_noisy_grid(100, 0.47)
    rule = mostly_walls
    iterations = 8

    print(f"Running program for {iterations} iterations.")
    states = run_automaton(initial_state, rule, iterations)
    render_result(states)


if __name__ == "__main__":
    main()
