"""
Generates environment
"""
import numpy as np
import random

def simple_relfex(dirty, up, down, right, left):
    """
    Memoryless, condition-action rule pairs
    Arbitrary rule selection: 
        clean if dirty, try in order to: move up, right, down, left
            In this scheme for 1D, the left movement will be proceeded by an immediate right movement

        If the map is >1D or the robot does not start at the left most square,
            this agent will not reach the goal state (all tiles clean)

    Parameters
    ----------
    dirty : bool
    up : bool
        able to move up
    right : bool
    down : bool
    left : bool

    Returns
    -------
    action : str
        one of ["clean", "up", "right", "down", "left", "no_action"]
    """

    if dirty:
        return "clean"
    elif up:
        return "up"
    elif right:
        return "right"
    elif left:
        return "left"
    elif down:
        return "down"
    else:
        return "no_action"

def randomized_reflex(up, down, right, left):
    actions = {"clean":True, "up":up, "right":right, "down":down, "left":left, "no_action":True}
    while True: # miniscule possibility of infinite loop if up,down,right,left not possible and we never pick clean & no_action
        choice = random.choice(actions.keys())
        if actions[choice]:
            return choice

def part_b():
    """
    Can a simple relfex agent with a randomized agent function outperform a simple reflex
        agent? Design such an agent and measure its performance on several envs.

    Yes, almost in all cases, having no sense of state leaves us in quite a bind.
        The simple reflex agent only performs rationally on a 1D map and depends on a convenient initial condition
    
    """
    pass

if __name__ == "__main__":
    part_b()