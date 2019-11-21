from __future__ import division
"""
Generates environment
"""
import numpy as np
import random
import time
import signal

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

def randomized_reflex(dirty, up, down, right, left):
    if dirty:
        return "clean"
    actions = {"clean":True, "up":up, "right":right, "down":down, "left":left}
    while True: # miniscule possibility of infinite loop if up,down,right,left not possible and we never pick clean & no_action
        choice = random.choice(actions.keys())
        if actions[choice]:
            return choice

def build_map(dirty_prob, map_type="rect", dims=(10,10)):
    """
    dims can also be (0,0) for random dimensions
    """
    
    if map_type == "rect":
        if dims == (0,0): # randomized case
            pass
        else:
            return np.random.choice(a=["*","_"], size=dims, p=[1 - dirty_prob, dirty_prob])
    else:
        # non rectangular map
        pass

def check_available_moves(agent_loc, map_dims):
    if agent_loc[0] == 0:
        up = False
    else:
        up = True
    if agent_loc[1] == 0:
        left = False
    else:
        left = True
    if agent_loc[0] == (map_dims[0] - 1):
        down = False
    else:
        down = True
    if agent_loc[1] == (map_dims[1] - 1):
        right = False
    else:
        right = True
    # print(agent_loc)
    # print(map_dims)
    # print(up)
    # print(down)
    # print(right)
    # print(left)
    return up, down, right, left

def execute_action(test_map, agent_loc, action):
    if action == "up":
        agent_loc[0] -= 1
    elif action == "down":
        agent_loc[0] += 1
    elif action == "left":
        agent_loc[1] -= 1
    elif action == "right":
        agent_loc[1] += 1
    elif action == "clean":
        test_map[agent_loc[0], agent_loc[1]] = '_'
    else:
        print("no action")
    return test_map, agent_loc

def simulate(test_map, start_loc, action_func):
    agent_loc = list(start_loc)
    g = GracefulKiller()
    num_loops = 0
    while test_map.__contains__("*") and not g.kill_now:
        num_loops += 1
        status = test_map[agent_loc[0], agent_loc[1]]
        if status == "*":
            dirty = True
        else:
            dirty = False
        # check bounds of map, check that wall (|) does not exist...
        up, down, right, left = check_available_moves(agent_loc, test_map.shape)
        action = action_func(dirty, up, down, right, left)
        test_map, agent_loc = execute_action(test_map, agent_loc, action)
        print_map = test_map.copy()
        print_map[agent_loc[0], agent_loc[1]] = "A"
        # print(print_map)
        # print("------------------------------------")
        # time.sleep(2)
    print(num_loops)


def part_b():
    """
    Can a simple relfex agent with a randomized agent function outperform a simple reflex
        agent? Design such an agent and measure its performance on several envs.

    Yes, almost in all cases, having no sense of state leaves us in quite a bind.
        The simple reflex agent only performs rationally on a 1D map and depends on a convenient initial condition

    Assume rectangular maps, else the randomized agent will have little to no change of completing

    Can I design an agent for non square maps as well? Should it map beforehand then fill in the gaps?
        Can I design a framework that maps & predicts spots
    
    """
    map_n = 5
    test_map = build_map(0.5, dims=(map_n,map_n))
    # choose random location for agent
    random_loc = np.random.randint(0, map_n**2)
    row = random_loc // map_n
    col = random_loc % map_n
    # simulate(test_map, (row, col), simple_relfex)
    simulate(test_map, (row, col), randomized_reflex)

# @credits: Mayank Jaiswal 2015 Stack Overflow
class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self,signum, frame):
    self.kill_now = True

if __name__ == "__main__":
    part_b()