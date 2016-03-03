import random
from environment import Agent, Environment, TrafficLight
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.q = {}
        valid_actions = Environment.valid_actions + [None]
        self.gamma = 0.9
        self.alpha = 0.2
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

        if self.first_iteration:
            self.first_iteration = False
        else:
            best_q = None
            for a_prime in self.q[self.state]:
                if best_q is None or self.q[self.state][a_prime] > best_q:
                    best_q = self.q[self.state][a_prime]
            self.q[self.prev_state][self.prev_action] = \
                self.q[self.prev_state][self.prev_action] + \
                self.alpha * (self.prev_reward + best_q - self.q[self.prev_state][self.prev_action])            
                
        # TODO: Select action according to your policy
        best_action = None
        best_q = 0
        for action in self.q[self.state]:
            if best_action is None or self.q[self.state][action] > best_q:
                best_action = action
                best_q = self.q[self.state][action]

        # Execute action and get reward
        reward = self.env.act(self, best_action)

        # TODO: Learn policy based on state, action, reward

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, best_action, reward)  # [debug]
        self.prev_state = self.state
        self.prev_action = best_action
        self.prev_reward = reward


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # set agent to track

    # Now simulate it
    sim = Simulator(e, update_delay=1.0)  # reduce update_delay to speed up simulation
    sim.run(n_trials=100)  # press Esc or close pygame window to quit


if __name__ == '__main__':
    run()
