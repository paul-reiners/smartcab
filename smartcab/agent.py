import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""
    
    AWESOME = 10.0

    def __init__(self, env, gamma):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # Initialize any additional variables here
        self.q = {}
        self.valid_actions = Environment.valid_actions + [None]
        self.gamma = gamma
        for left in self.valid_actions:
            for right in self.valid_actions:
                for oncoming in self.valid_actions:
                    for light in ['green', 'red']:
                        for next_waypoint in Environment.valid_actions[1:]:
                            state = (left, right, oncoming, light, next_waypoint)
                            self.q[state] = {}
                            for action in self.valid_actions:
                                # optimism in the face of uncertainty
                                # See https://youtu.be/ws5BOy6L_V0?t=1m37s
                                self.q[state][action] = self.AWESOME
        self.t = 1 
        self.epsilon = 0.5   
        self.initialize()
        
    def initialize(self):
        self.state = None
        self.total_reward = 0

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # Prepare for a new trip; reset any variables here, if required
        self.initialize()

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # Update state
        self.state = (inputs['left'], inputs['right'], inputs['oncoming'], inputs['light'], self.next_waypoint)

        # Select action according to your policy
        best_action = self.epsilon_greedy_exploration(self.state, self.epsilon)
        # GLIE (decayed epsilon)
        self.epsilon *= 0.99

        # Execute action and get reward
        reward = self.env.act(self, best_action)

        # Learn policy based on state, action, reward
        s = self.state
        a = best_action
        r = reward
        next_waypoint = self.planner.next_waypoint()  
        inputs = self.env.sense(self)
        
        # Calculate next state, s'
        s_prime = (inputs['left'], inputs['right'], inputs['oncoming'], inputs['light'], next_waypoint)
        utility_of_next_state = self.get_utility_of_next_state(s_prime)
        utility_of_state = r + self.gamma * utility_of_next_state
        # Learning rate decays over time
        learning_rate = get_learning_rate(self.t)
        # Adjust Q table
        self.q[s][a] = modify_by_learning_rate(learning_rate, self.q[s][a], utility_of_state)
        
        self.t += 1
        
        self.total_reward += reward
        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}, total_reward = {}".format(deadline, inputs, best_action, reward, self.total_reward)  # [debug]


    def greedy_policy(self, state):
        best_action = None
        best_q = None
        for action in self.q[state]:
            if best_q is None or self.q[state][action] > best_q:
                best_action = action
                best_q = self.q[state][action]
        
        return best_action
    
    
    def epsilon_greedy_exploration(self, state, epsilon):
        if random.random() < epsilon:
            return random.choice(self.valid_actions)
        else:
            return self.greedy_policy(state)
    
    
    def get_utility_of_next_state(self, s_prime):
        best_utility_of_next_state = None
        for a_prime in self.q[s_prime]:
            if best_utility_of_next_state is None or self.q[s_prime][a_prime] > best_utility_of_next_state:
                best_utility_of_next_state = self.q[s_prime][a_prime]
        utility_of_next_state = best_utility_of_next_state
        
        return utility_of_next_state


def get_learning_rate(t):
    return 1.0 / float(t)


def modify_by_learning_rate(learning_rate, v, x):
    return (1 - learning_rate) * v + learning_rate * x


def run(gamma):
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent, gamma=gamma)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # set agent to track

    # Now simulate it
    sim = Simulator(e, update_delay=0.1)  # reduce update_delay to speed up simulation
    sim.run(n_trials=10)  # press Esc or close pygame window to quit


if __name__ == '__main__':
    gamma = 0.9
    run(gamma=gamma)
