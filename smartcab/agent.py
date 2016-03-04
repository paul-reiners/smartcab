import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
import sys

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env, gamma, alpha):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.q = {}
        valid_actions = Environment.valid_actions + [None]
        self.gamma = gamma
        self.alpha = alpha
        for left in valid_actions:
            for right in valid_actions:
                for oncoming in valid_actions:
                    for light in ['green', 'red']:
                        for next_waypoint in Environment.valid_actions[1:]:
                            state = (left, right, oncoming, light, next_waypoint)
                            self.q[state] = {}
                            for action in valid_actions:
                                self.q[state][action] = 0.0
            
        self.initialize()
        
    def initialize(self):
        self.state = None
        self.prev_state = None
        self.prev_action = None
        self.prev_reward = None
        self.first_iteration = True
        self.total_reward = 0

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.initialize()

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        self.state = (inputs['left'], inputs['right'], inputs['oncoming'], inputs['light'], self.next_waypoint)

        # TODO: Select action according to your policy
        best_action = None
        best_q = None
        for action in self.q[self.state]:
            if best_q is None or self.q[self.state][action] > best_q:
                best_action = action
                best_q = self.q[self.state][action]

        # Execute action and get reward
        reward = self.env.act(self, best_action)

        # TODO: Learn policy based on state, action, reward
        s = self.state
        a = best_action
        r = reward
        next_waypoint = self.planner.next_waypoint()  
        inputs = self.env.sense(self)
        s_prime = (inputs['left'], inputs['right'], inputs['oncoming'], inputs['light'], next_waypoint)
        utility_of_next_state = self.get_utility_of_next_state(s_prime)
        utility_of_state = r + self.gamma * utility_of_next_state
        self.q[s][a] = modify_by_alpha(self.alpha, self.q[s][a], utility_of_state)
        
        self.total_reward += reward
        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}, total_reward = {}".format(deadline, inputs, best_action, reward, self.total_reward)  # [debug]
        self.prev_state = self.state
        self.prev_action = best_action
        self.prev_reward = reward


    def get_utility_of_next_state(self, s_prime):
        best_utility_of_next_state = None
        for a_prime in self.q[s_prime]:
            if best_utility_of_next_state is None or self.q[s_prime][a_prime] > best_utility_of_next_state:
                best_utility_of_next_state = self.q[s_prime][a_prime]
        utility_of_next_state = best_utility_of_next_state
        
        return utility_of_next_state


def modify_by_alpha(alpha, v, x):
    return (1 - alpha) * v + alpha * x

def run(gamma, alpha):
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent, gamma=gamma, alpha=alpha)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # set agent to track

    # Now simulate it
    sim = Simulator(e, update_delay=0.1)  # reduce update_delay to speed up simulation
    sim.run(n_trials=100)  # press Esc or close pygame window to quit


if __name__ == '__main__':
    gamma = float(sys.argv[1])
    alpha = float(sys.argv[2])
    run(gamma=gamma, alpha=alpha)
