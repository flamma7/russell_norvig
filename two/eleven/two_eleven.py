from __future__ import division
"""
Generates environment
"""
import numpy as np
import random
import time
import signal
import sys

"""
TODO
- map printing is functional, add current position printing
- map extending appears to be disfunctional atm as well
- once I can map out the entire map via moving around --> add decision logic
"""

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

class SensorMeas:
    def __init__(self, dirty, up, down, right, left):
        self.dirty = dirty
        self.up = up
        self.down = down
        self.right = right
        self.left = left

# defines
WALL      = 3
DIRTY     = 2
CLEAN     = 1
UNKNOWN   = 0

class RationAgent:
    def __init__(self):
        self.responce_number = 0
        self.seq = 0
        self.state = 0
        self.map = np.zeros((3,3))
        self.current_pos = [1,1]

    def determine_response_number(self, meas):
        total = int(meas.up) + int(meas.down) + int(meas.right) + int(meas.left)
        if total > 1:
            self.responce_number = 1
        elif total:
            self.responce_number = 2
        else:
            self.responce_number = 3

    def update_map(self, meas):
        """ Marks Walls and clean/dirty on the map """
        # print("Current meas:")
        # print("d: " + str(meas.dirty))
        # print("up: " + str(meas.up))
        # print("down: " + str(meas.down))
        # print("right: " + str(meas.right))
        # print("left: " + str(meas.left))

        x = self.current_pos[0]
        y = self.current_pos[1]
        if meas.dirty:
            self.map[x,y] = DIRTY
        else:
            self.map[x,y] = CLEAN
        
        if not meas.up:
            self.map[x-1,y] = WALL
        elif not meas.down:
            self.map[x+1,y] = WALL
        if not meas.right:
            self.map[x,y+1] = WALL
        elif not meas.left:
            self.map[x,y-1] = WALL
    
    def test_map_building(self, dirty):
        """ Gets the action via key motion from the user """
        while True:
            print("-------------------------")
            if dirty:
                print("Square is dirty")
            key = raw_input("Next motion: (w,a,s,d, c for clean, q for quit)\n")
            if key == "w":
                motion = "up"
            elif key == "a":
                motion = "left"
            elif key == "d":
                motion = "right"
            elif key == "s":
                motion = "down"
            elif key == "c":
                return "clean"
            elif key == "q":
                sys.exit(1)
            else:
                print("Unrecognized input key: " + key)
                continue

            if self.determine_valid_motion(motion):
                return motion
            else:
                print("You ran into a wall!")

    def print_map(self):
        map_str = np.empty(self.map.shape, dtype="|S1")
        [x,y] = self.map.shape
        for i in range(self.map.size):
            if self.map.flatten()[i] == WALL:
                map_str[i//y, i % y] = "X"
            elif self.map.flatten()[i] == UNKNOWN:
                map_str[i//y, i % y] = " "
            elif self.map.flatten()[i] == DIRTY:
                map_str[i//y, i % y] = "*"
            elif self.map.flatten()[i] == CLEAN:
                map_str[i//y, i % y] = "_"
        print("DIRTY: *\tCLEAN: _\tWALL: X")
        map_str[self.current_pos[0], self.current_pos[1]] = "A"
        print(map_str)

    def determine_valid_motion(self, motion):
        [x,y] = self.current_pos
        if motion == "up" and self.map[x-1,y] == WALL:
            return False
        elif motion == "down" and self.map[x+1,y] == WALL:
            return False
        elif motion == "left" and self.map[x,y-1] == WALL:
            return False
        elif motion == "right" and self.map[x,y+1] == WALL:
            return False
        else:
            return True

    def handle_motion(self, motion):
        """ Updates the current position and grows the map """

        if motion == "clean":
            pass
        elif motion == "up":
            if self.current_pos[0] - 2 < 0: # grow map upwards
                self.map = np.append(np.zeros( (1,self.map.shape[1]) ), self.map, axis=0)
                # NOTE, adjusting the map here also moves the position
            else:
                self.current_pos[0] -= 1
                
        elif motion == "down":
            self.current_pos[0] += 1
            if self.current_pos[0] + 2 > self.map.shape[0]: # grow map downwards
                self.map = np.append(self.map, np.zeros((1, self.map.shape[1])), axis=0)

        elif motion == "left":
            if self.current_pos[1] - 2 < 0: # grow map leftwards
                self.map = np.append(np.zeros( (self.map.shape[0],1)), self.map, axis=1)
                # NOTE, adjusting the map here also moves the position
            else:
                self.current_pos[1] -= 1

        elif motion == "right":
            self.current_pos[1] += 1
            if self.current_pos[1] + 2 > self.map.shape[1]: # grow map rightwards
                self.map = np.append(self.map, np.zeros((self.map.shape[0],1)), axis=1)

    def reflex_type1(self, meas): # start in corner
        if meas.dirty:
            return "clean"
        
    def reflex_type2(self, meas): # start on edge
        pass

    def reflex_type3(self, meas): # start in darkness
        pass
 
    def rational_reflex(self, meas):
        """ meas : SensorMeas Type """
        if self.responce_number == 0:
            self.determine_response_number(meas)
            print("response #: " + str(self.responce_number))

        self.seq += 1

        # Respond
        self.update_map(meas)
        self.print_map()
        motion = self.test_map_building(meas.dirty)
        self.handle_motion(motion)
        
        return motion

        # if self.responce_number == 1:
        #     self.reflex_type1(meas)
        # elif self.responce_number == 2:
        #     self.reflex_type2(meas)
        # elif self.responce_number == 3:
        #     self.reflex_type3(meas)
        # else:
        #     raise(Exception("Unrecognized response number"))

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
        action = action_func( SensorMeas(dirty, up, down, right, left) )
        test_map, agent_loc = execute_action(test_map, agent_loc, action)
        # print_map = test_map.copy()
        # print_map[agent_loc[0], agent_loc[1]] = "A"
        # print(print_map)
        # print("------------------------------------")
        # time.sleep(2)
    print(str(num_loops) + " moves taken")


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
    map_n = 3
    test_map = build_map(0.5, dims=(map_n,map_n))
    # choose random location for agent
    random_loc = np.random.randint(0, map_n**2)
    row = random_loc // map_n
    col = random_loc % map_n
    # simulate(test_map, (row, col), simple_relfex)
    # simulate(test_map, (row, col), randomized_reflex)
    r = RationAgent()
    simulate(test_map, (row, col), r.rational_reflex)

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